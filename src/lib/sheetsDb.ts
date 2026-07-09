import { getAccessToken } from './googleAuth';
const SPREADSHEET_ID = '1sWm_oJ0R59r9pWKuAiNko9tuEL952uqflDBa6MfqGVM';
async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const token = getAccessToken();
  if (!token) throw new Error('Not authenticated with Google');
    const headers = {
    ...options.headers,
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json',
  };
    const response = await fetch(url, { ...options, headers });
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Google Sheets API Error: ${response.status} ${errorText}`);
  }
  return response.json();
}
async function ensureHeaders(sheetName: string, headers: string[]) {
  const res = await fetchWithAuth(`https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/${sheetName}!A1:Z1`);
  const currentHeaders = res.values && res.values.length > 0 ? res.values[0] : [];
  if (currentHeaders.length < headers.length) { 
    await fetchWithAuth(`https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/${sheetName}!A1?valueInputOption=USER_ENTERED`, { 
      method: "PUT", 
      body: JSON.stringify({ values: [headers] }) 
    });
  }
}
export async function initializeSheets() {
  const meta = await fetchWithAuth(`https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}`);
  const existingSheetTitles = meta.sheets.map((s: any) => s.properties.title);
    const requiredSheets = [
    { title: 'Users', headers: ['id', 'username', 'password', 'name', 'role', 'createdAt', 'updatedAt', 'accountType', 'affiliation', 'status'] },
    { title: 'ST5', headers: ['id', 'userId', 'score', 'answers', 'timestamp'] },
    { title: 'Behaviors', headers: ['id', 'targetUid', 'targetName', 'selections', 'timestamp'] }
  ];
  const requests = [];
  for (const sheet of requiredSheets) {
    if (!existingSheetTitles.includes(sheet.title)) {
      requests.push({
        addSheet: {
          properties: { title: sheet.title }
        }
      });
    }
  }
  for (const sheet of requiredSheets) {
    if (existingSheetTitles.includes(sheet.title)) {
      await ensureHeaders(sheet.title, sheet.headers);
    }
  }
  if (requests.length > 0) {
    await fetchWithAuth(`https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}:batchUpdate`, {
      method: 'POST',
      body: JSON.stringify({ requests })
    });
        for (const sheet of requiredSheets) {
      if (!existingSheetTitles.includes(sheet.title)) {
        await fetchWithAuth(`https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/${sheet.title}!A1:append?valueInputOption=USER_ENTERED`, {
          method: 'POST',
          body: JSON.stringify({
            values: [sheet.headers]
          })
        });
      }
    }
  }
}
export async function appendRow(sheetName: string, rowData: any[]) {
  const safeData = rowData.map(v => (v === undefined || v === null) ? "" : v);
  await fetchWithAuth(`https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/${sheetName}!A1:append?valueInputOption=USER_ENTERED`, {
    method: 'POST',
    body: JSON.stringify({
      values: [safeData]
    })
  });
}
export async function getRows(sheetName: string): Promise<any[]> {
  try {
    const res = await fetchWithAuth(`https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/${sheetName}!A1:Z`);
    const rows = res.values || [];
    if (rows.length === 0) return [];
        const headers = rows[0];
    const data = [];
    for (let i = 1; i < rows.length; i++) {
      const obj: any = { _rowIndex: i + 1 };
      for (let j = 0; j < headers.length; j++) {
        let val = rows[i][j];
        if (val !== undefined && val !== null && val.startsWith && val.startsWith('{')) { 
          try { val = JSON.parse(val); } catch(e) {}
        } else if (val !== undefined && val !== null && val.startsWith && val.startsWith('[')) { 
          try { val = JSON.parse(val); } catch(e) {}
        }
        obj[headers[j]] = val;
      }
      data.push(obj);
    }
    return data;
  } catch (e) {
    console.error("Error reading from Google Sheets", e);
    throw e;
  }
}
export async function updateRow(sheetName: string, rowIndex: number, rowData: any[]) {
  const safeData = rowData.map(v => (v === undefined || v === null) ? "" : v);
  await fetchWithAuth(`https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/${sheetName}!A${rowIndex}?valueInputOption=USER_ENTERED`, {
    method: 'PUT',
    body: JSON.stringify({
      values: [safeData]
    })
  });
}
export async function deleteRow(sheetName: string, rowIndex: number, sheetId: number) {
  await fetchWithAuth(`https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}:batchUpdate`, {
    method: 'POST',
    body: JSON.stringify({
      requests: [{
        deleteDimension: {
          range: {
            sheetId: sheetId,
            dimension: "ROWS",
            startIndex: rowIndex - 1,
            endIndex: rowIndex
          }
        }
      }]
    })
  });
}
export async function getSheetId(sheetName: string): Promise<number> {
  const meta = await fetchWithAuth(`https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}`);
  const sheet = meta.sheets.find((s: any) => s.properties.title === sheetName);
  return sheet ? sheet.properties.sheetId : 0;
}
