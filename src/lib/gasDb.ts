// gasDb.ts
// This module acts as a drop-in replacement for Firestore, bridging to Google Apps Script.

export const GAS_URL: string = "https://script.google.com/macros/s/AKfycbxFPnJm9fQloA3vEbM909DJLelsfN6nWSmJ6cLgEYojFZq-pcwza93rQmca4np7H-NC/exec";

// In-memory cache for GET queries to avoid concurrent execution rate limits on Google Apps Script
const getCache = new Map<string, { timestamp: number; data: any }>();
const inFlightRequests = new Map<string, Promise<any>>();
const CACHE_TTL_MS = 10000; // 10 seconds cache for GET requests

export function invalidateCache(sheetName?: string) {
  if (sheetName) {
    getCache.delete(sheetName);
  } else {
    getCache.clear();
  }
}

export async function gasRequest(action: string, sheetName: string, data: any = {}, retryCount = 2): Promise<any> {
  if (!GAS_URL || GAS_URL === '') {
    throw new Error('Please set GAS_URL in src/lib/gasDb.ts');
  }

  // Handle in-flight request deduplication and caching for GET actions
  if (action === 'GET') {
    const cached = getCache.get(sheetName);
    if (cached && (Date.now() - cached.timestamp < CACHE_TTL_MS)) {
      return cached.data;
    }
    const inFlight = inFlightRequests.get(sheetName);
    if (inFlight) {
      return inFlight;
    }
  } else {
    // Invalidate cache when modifying data
    invalidateCache(sheetName);
  }

  const executeRequest = async (): Promise<any> => {
    let lastError: any = null;
    for (let attempt = 0; attempt <= retryCount; attempt++) {
      try {
        if (attempt > 0) {
          // Exponential backoff
          await new Promise(resolve => setTimeout(resolve, attempt * 1000));
        }

        const response = await fetch(GAS_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'text/plain;charset=utf-8' // important for avoiding CORS preflight
          },
          body: JSON.stringify({ action, sheetName, data })
        });

        if (!response.ok) {
          throw new Error(`HTTP error ${response.status}`);
        }

        const text = await response.text();
        
        // If Google Apps Script returned a plain text fallback like "Mental Care API is running!"
        // or an HTML error page, retry
        let result: any;
        try {
          result = JSON.parse(text);
        } catch (jsonErr) {
          if (attempt < retryCount) {
            console.warn(`[gasDb] Non-JSON response for ${action} ${sheetName}, retrying (${attempt + 1}/${retryCount})...`);
            continue;
          }
          // If we have stale cache, return it instead of throwing fatal error
          const stale = getCache.get(sheetName);
          if (action === 'GET' && stale) {
            console.warn(`[gasDb] Using stale cache for ${sheetName} due to parse error`);
            return stale.data;
          }
          throw new Error('ไม่สามารถเชื่อมต่อฐานข้อมูล Google Sheet ได้ (โปรดตรวจสอบการเชื่อมต่ออินเทอร์เน็ต หรือลองใหม่อีกครั้ง)');
        }

        if (!result.success) {
          throw new Error(`Google Apps Script Error: ${result.error || 'Unknown Error'}`);
        }

        if (action === 'GET') {
          getCache.set(sheetName, { timestamp: Date.now(), data: result.data || [] });
        }

        return result.data;
      } catch (err: any) {
        lastError = err;
        if (attempt < retryCount) {
          console.warn(`[gasDb] Request failed (${attempt + 1}/${retryCount}), retrying...`, err.message);
        }
      }
    }

    // If all retries failed but we have stale cache for GET, return it
    const stale = getCache.get(sheetName);
    if (action === 'GET' && stale) {
      console.warn(`[gasDb] Using stale cache for ${sheetName} after all retries failed`);
      return stale.data;
    }

    throw lastError || new Error('ไม่สามารถเชื่อมต่อฐานข้อมูล Google Sheet ได้');
  };

  if (action === 'GET') {
    const promise = executeRequest().finally(() => {
      inFlightRequests.delete(sheetName);
    });
    inFlightRequests.set(sheetName, promise);
    return promise;
  }

  return executeRequest();
}

export const getFirestore = () => ({});
export const collection = (db: any, ...paths: string[]) => paths;
export const doc = (db: any, ...paths: string[]) => paths;

const getSheetName = (paths: string[]) => {
  const name = paths[4];
  if (name === 'users') return 'Users';
  if (name === 'st5') return 'ST5';
  if (name === 'behaviors') return 'Behaviors';
  return name || 'Unknown';
};

const parseDateString = (dateStr: any) => {
  if (!dateStr) return Date.now();
  if (typeof dateStr === 'number') return dateStr;
  const str = String(dateStr);
  const parts = str.split(' ');
  if (parts.length >= 2) {
      const [d, t] = parts;
      const [day, mo, yr] = d.split('/');
      const [h, m, s] = t.split(':');
      const year = Number(yr) > 2500 ? Number(yr) - 543 : Number(yr); // Handle Thai Buddhist Year if present
      const dateObj = new Date(year, Number(mo)-1, Number(day), Number(h), Number(m), Number(s));
      if (!isNaN(dateObj.getTime())) return dateObj.getTime();
  }
  return new Date(str).getTime() || Date.now();
};

const formatRowOut = (row: any) => {
  if (!row) return row;
  try {
      if (row.timestamp && typeof row.timestamp === 'string') {
        row.timestamp = parseDateString(row.timestamp);
      }
      if (row.createdAt && typeof row.createdAt === 'string') {
        row.createdAt = parseDateString(row.createdAt);
      }
  } catch (err) {
      console.error("formatRowOut error:", err, row);
  }
  return row;
};

export const getDoc = async (paths: string[]) => {
  const sheetName = getSheetName(paths);
  const docId = paths[5];
  const rows = await gasRequest('GET', sheetName);
  const row = (rows || []).find((r: any) => String(r.id) === String(docId));
  if (row) {
    return { exists: () => true, id: docId, data: () => formatRowOut(row) };
  }
  return { exists: () => false, id: docId, data: () => null };
};

export const getDocs = async (paths: string[]) => {
  const sheetName = getSheetName(paths);
  const rows = await gasRequest('GET', sheetName);
  const docs = (rows || []).map((r: any) => ({ id: r.id, data: () => formatRowOut(r) }));
  return { docs, forEach: (cb: any) => docs.forEach(cb) };
};

const formatRowIn = (data: any) => {
  if (!data) return data;
  return { ...data };
};

export const setDoc = async (paths: string[], data: any) => {
  const sheetName = getSheetName(paths);
  const docId = paths[5];
  
  const rows = await gasRequest('GET', sheetName);
  const exists = (rows || []).find((r: any) => String(r.id) === String(docId));
  
  const payload = { id: docId, ...formatRowIn(data) };
  if (exists) {
    await gasRequest('UPDATE', sheetName, payload);
  } else {
    await gasRequest('ADD', sheetName, payload);
  }
};

export const updateDoc = async (paths: string[], data: any) => {
  const sheetName = getSheetName(paths);
  const docId = paths[5];
  const payload = { id: docId, ...formatRowIn(data) };
  await gasRequest('UPDATE', sheetName, payload);
};

export const addDoc = async (paths: string[], data: any) => {
  const sheetName = getSheetName(paths);
  const newId = Math.random().toString(36).substring(2, 15);
  const payload = { id: newId, ...formatRowIn(data) };
  await gasRequest('ADD', sheetName, payload);
  return { id: newId };
};

export const deleteDoc = async (paths: string[]) => {
  const sheetName = getSheetName(paths);
  const docId = paths[5];
  await gasRequest('DELETE', sheetName, { id: docId });
};

export const onSnapshot = (paths: string[], callback: (snap: any) => void) => {
  let isCancelled = false;
  const poll = async () => {
    if (isCancelled) return;
    try {
      const snap = await getDocs(paths);
      if (!isCancelled) callback(snap);
    } catch(e) {
      console.error("onSnapshot error", e);
    }
    if (!isCancelled) setTimeout(poll, 15000); 
  };
  poll(); // start immediately
  return () => { isCancelled = true; };
};
