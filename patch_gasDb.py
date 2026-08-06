import sys

with open('src/lib/gasDb.ts', 'r') as f:
    content = f.read()

old_gasRequest = """export async function gasRequest(action: string, sheetName: string, data: any = {}) {
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
  
  if (!result.success) throw new Error(`Google Apps Script Error: ${result.error || 'Unknown Error'}. โปรดตรวจสอบว่าได้อัปเดตโค้ดใน Apps Script ล่าสุดและ Deploy เป็น New deployment แล้ว`);
  return result.data;
}"""

new_gasRequest = """// Cache for GET requests
let cachedSyncData: any = null;
let lastSyncTime = 0;

export async function gasRequest(action: string, sheetName: string, data: any = {}) {
  if (!GAS_URL || GAS_URL === '') {
    throw new Error('Please set GAS_URL in src/lib/gasDb.ts');
  }
  
  if (action === 'GET') {
      try {
          const now = Date.now();
          if (cachedSyncData && now - lastSyncTime < 5000) {
              // use cache if less than 5 seconds old
          } else {
              const response = await fetch(GAS_URL + "?action=sync");
              cachedSyncData = await response.json();
              lastSyncTime = now;
          }
          
          if (cachedSyncData && cachedSyncData.success) {
              let rows = [];
              if (sheetName === 'Users') rows = cachedSyncData.users || [];
              else if (sheetName === 'ST5') rows = cachedSyncData.st5 || [];
              else if (sheetName === 'Behaviors') rows = cachedSyncData.behaviors || [];
              return rows;
          }
      } catch (e) {
          console.error("GET sync failed", e);
      }
      return [];
  }
  
  let response;
  try {
    response = await fetch(GAS_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'text/plain;charset=utf-8'
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
  
  if (result.success === true || result.status === 'success') {
      return result.data || [];
  }
  
  throw new Error(`Google Apps Script Error: ${result.error || 'Unknown Error'}. โปรดตรวจสอบว่าได้อัปเดตโค้ดใน Apps Script ล่าสุดและ Deploy เป็น New deployment แล้ว`);
}"""

if old_gasRequest in content:
    content = content.replace(old_gasRequest, new_gasRequest)
    with open('src/lib/gasDb.ts', 'w') as f:
        f.write(content)
    print("Patch applied to src/lib/gasDb.ts")
else:
    print("Could not find the target text in src/lib/gasDb.ts.")
