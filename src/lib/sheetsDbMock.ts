import { getRows, appendRow, updateRow, deleteRow } from './sheetsDb';
export const getFirestore = (...args: any[]) => ({});
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
  const rows = await getRows(sheetName);
  const row = rows.find(r => String(r.id) === String(docId));
  if (row) {
    return { exists: () => true, id: docId, data: () => row };
  }
  return { exists: () => false, id: docId, data: () => null };
};
export const getDocs = async (paths: string[]) => {
  const sheetName = getSheetName(paths);
  const rows = await getRows(sheetName);
  const docs = rows.map(r => ({ id: r.id, data: () => r }));
  return {
    docs,
    forEach: (cb: any) => docs.forEach(cb)
  };
};
const mapValues = (sheetName: string, finalData: any) => {
  let values: any[] = [];
  if (sheetName === 'Users') {
    values = [finalData.id, finalData.username, finalData.password, finalData.name, finalData.role, finalData.createdAt, finalData.updatedAt, finalData.accountType, finalData.affiliation, finalData.status];
  } else if (sheetName === 'ST5') {
    values = [finalData.id, finalData.userId || finalData.uid, finalData.score, typeof finalData.answers === 'string' ? finalData.answers : JSON.stringify(finalData.answers), finalData.timestamp];
  } else if (sheetName === 'Behaviors') {
    values = [finalData.id, finalData.targetUid || finalData.uid, finalData.targetName || finalData.name, typeof finalData.selections === 'string' ? finalData.selections : JSON.stringify(finalData.selections), finalData.timestamp];
  } else {
    values = [finalData.id, JSON.stringify(finalData)];
  }
  return values;
};
export const setDoc = async (paths: string[], data: any) => {
  const sheetName = getSheetName(paths);
  const docId = paths[5];
  const rows = await getRows(sheetName);
  const row = rows.find(r => String(r.id) === String(docId));
  const finalData = { id: docId, ...data };
    const values = mapValues(sheetName, finalData);
  if (row) {
    await updateRow(sheetName, row._rowIndex, values);
  } else {
    await appendRow(sheetName, values);
  }
};
export const updateDoc = async (paths: string[], data: any) => {
  const sheetName = getSheetName(paths);
  const docId = paths[5];
  const rows = await getRows(sheetName);
  const row = rows.find(r => String(r.id) === String(docId));
  if (!row) throw new Error("Document not found");
    const finalData = { ...row, ...data };
  const values = mapValues(sheetName, finalData);
  await updateRow(sheetName, row._rowIndex, values);
};
export const addDoc = async (paths: string[], data: any) => {
  const sheetName = getSheetName(paths);
  const newId = Math.random().toString(36).substring(2, 15);
  const finalData = { id: newId, ...data };
    const values = mapValues(sheetName, finalData);
  await appendRow(sheetName, values);
  return { id: newId };
};
export const deleteDoc = async (paths: string[]) => {
  const sheetName = getSheetName(paths);
  const docId = paths[5];
  const rows = await getRows(sheetName);
  const row = rows.find(r => String(r.id) === String(docId));
  if (row) {
    await updateRow(sheetName, row._rowIndex, ['', '', '', '', '', '', '']);
  }
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
    if (!isCancelled) setTimeout(poll, 60000);
  };
  poll();
  return () => { isCancelled = true; };
};
