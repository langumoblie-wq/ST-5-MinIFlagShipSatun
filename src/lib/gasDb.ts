// gasDb.ts
// This module acts as a drop-in replacement for Firestore, bridging to Google Apps Script.

export const GAS_URL: string = 'https://script.google.com/macros/s/AKfycbwxo4W3kBt6GvnGBdIkkjhLh3F8k_4jW1-nxyLKcG4UDXcGbargd6QiftPxV4NopIFr/exec'; // User must replace this!

export async function gasRequest(action: string, sheetName: string, data?: any) {
  if (!GAS_URL || GAS_URL === '') {
    throw new Error('Please set GAS_URL in src/lib/gasDb.ts');
  }
  
  let response;
  try {
    response = await fetch(GAS_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'text/plain;charset=utf-8' // important for avoiding CORS preflight
      },
      body: JSON.stringify({ action, sheetName, data })
    });
  } catch (e) {
    throw new Error('ไม่สามารถเชื่อมต่อฐานข้อมูลได้ (โปรดตรวจสอบว่าตั้งค่า Google Apps Script > Who has access: Anyone)');
  }
  
  let result;
  try {
    const text = await response.text();
    result = JSON.parse(text);
  } catch (e) {
    throw new Error('ไม่สามารถเชื่อมต่อฐานข้อมูล Google Sheet ได้ (โปรด Deploy สคริปต์ใหม่ แล้วนำ URL มาตั้งค่าใหม่)');
  }
  
  if (!result.success) throw new Error(result.error);
  return result.data;
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

export const getDoc = async (paths: string[]) => {
  const sheetName = getSheetName(paths);
  const docId = paths[5];
  const rows = await gasRequest('GET', sheetName);
  const row = rows.find((r: any) => String(r.id) === String(docId));
  if (row) {
    return { exists: () => true, id: docId, data: () => row };
  }
  return { exists: () => false, id: docId, data: () => null };
};

export const getDocs = async (paths: string[]) => {
  const sheetName = getSheetName(paths);
  const rows = await gasRequest('GET', sheetName);
  const docs = (rows || []).map((r: any) => ({ id: r.id, data: () => r }));
  return { docs, forEach: (cb: any) => docs.forEach(cb) };
};

export const setDoc = async (paths: string[], data: any) => {
  const sheetName = getSheetName(paths);
  const docId = paths[5];
  
  const rows = await gasRequest('GET', sheetName);
  const exists = rows.find((r: any) => String(r.id) === String(docId));
  
  const payload = { id: docId, ...data };
  if (exists) {
    await gasRequest('UPDATE', sheetName, payload);
  } else {
    await gasRequest('ADD', sheetName, payload);
  }
};

export const updateDoc = async (paths: string[], data: any) => {
  const sheetName = getSheetName(paths);
  const docId = paths[5];
  const payload = { id: docId, ...data };
  await gasRequest('UPDATE', sheetName, payload);
};

export const addDoc = async (paths: string[], data: any) => {
  const sheetName = getSheetName(paths);
  const newId = Math.random().toString(36).substring(2, 15);
  const payload = { id: newId, ...data };
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
