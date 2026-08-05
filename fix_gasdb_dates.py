import sys

with open('src/lib/gasDb.ts', 'r') as f:
    content = f.read()

old_get = """export const getDoc = async (paths: string[]) => {
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
};"""

new_get = """const parseDateString = (dateStr: any) => {
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
  if (row.timestamp && typeof row.timestamp === 'string') {
    row.timestamp = parseDateString(row.timestamp);
  }
  if (row.createdAt && typeof row.createdAt === 'string') {
    row.createdAt = parseDateString(row.createdAt);
  }
  return row;
};

export const getDoc = async (paths: string[]) => {
  const sheetName = getSheetName(paths);
  const docId = paths[5];
  const rows = await gasRequest('GET', sheetName);
  const row = rows.find((r: any) => String(r.id) === String(docId));
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
};"""

old_set = """export const setDoc = async (paths: string[], data: any) => {
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
};"""

new_set = """const formatDateForSheet = (ts: any) => {
  if (!ts) return '';
  const d = new Date(ts);
  if (isNaN(d.getTime())) return ts;
  return d.toLocaleString('th-TH', { 
      day: '2-digit', month: '2-digit', year: 'numeric',
      hour: '2-digit', minute: '2-digit', second: '2-digit'
  });
};

const formatRowIn = (data: any) => {
  const payload = { ...data };
  if (payload.timestamp && typeof payload.timestamp === 'number') {
    payload.timestamp = formatDateForSheet(payload.timestamp);
  }
  if (payload.createdAt && typeof payload.createdAt === 'number') {
    payload.createdAt = formatDateForSheet(payload.createdAt);
  }
  return payload;
};

export const setDoc = async (paths: string[], data: any) => {
  const sheetName = getSheetName(paths);
  const docId = paths[5];
  
  const rows = await gasRequest('GET', sheetName);
  const exists = rows.find((r: any) => String(r.id) === String(docId));
  
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
};"""

if old_get in content and old_set in content:
    content = content.replace(old_get, new_get)
    content = content.replace(old_set, new_set)
    with open('src/lib/gasDb.ts', 'w') as f:
        f.write(content)
    print("Successfully patched gasDb.ts")
else:
    print("Could not find old contents in gasDb.ts")
