// โค้ด Google Apps Script สำหรับเป็น API ให้กับ Mental Care Web App
// คัดลอกโค้ดนี้ทั้งหมดไปใส่ใน Google Apps Script
// จากนั้นกด Deploy -> New deployment -> เลือกประเภท Web App
// Execute as: Me (ตัวฉันเอง)
// Who has access: Anyone (ทุกคน)

// !!! ฟังก์ชันสำหรับขอสิทธิ์ (รันฟังก์ชันนี้ครั้งแรกเพื่อขอสิทธิ์) !!!
function setup() {
  // เรียกใช้งาน DriveApp เพื่อให้ Google Apps Script ขอสิทธิ์การจัดการไฟล์แบบเต็ม
  var tempFolder = DriveApp.createFolder("Temp_Mental_Care_Setup");
  tempFolder.setTrashed(true);
  
  // เรียกใช้งาน SpreadsheetApp เพื่อขอสิทธิ์จัดการ Google Sheets
  SpreadsheetApp.getActiveSpreadsheet();
  
  console.log("ตั้งค่าและให้สิทธิ์สำเร็จ");
}

function doPost(e) {
  try {
    var params = JSON.parse(e.postData.contents);
    var action = params.action;
    var data = params.data || {};
    
    // --- 1. ฟังก์ชันสำหรับอัปโหลด PDF ไปยัง Google Drive ---
    if (action === 'UPLOAD_PDF') {
      var filename = data.filename || params.filename || "Consent_Form.pdf";
      var base64 = data.base64 || params.base64;
      
      if (!base64) {
         return ContentService.createTextOutput(JSON.stringify({
            success: false, error: "Missing base64 data"
         })).setMimeType(ContentService.MimeType.JSON);
      }
      
      var decoded = Utilities.base64Decode(base64);
      var blob = Utilities.newBlob(decoded, 'application/pdf', filename);
      var folder = DriveApp.getFolderById("1l8KRC-3pROwNTgWqRJvHa9vM6CqdTttn");
      var file = folder.createFile(blob);
      
      return ContentService.createTextOutput(JSON.stringify({
        success: true,
        fileUrl: file.getUrl()
      })).setMimeType(ContentService.MimeType.JSON);
    }
    
    // --- 2. ฟังก์ชันสำหรับจัดการฐานข้อมูล (Drop-in Firestore) ---
    var sheetName = params.sheetName;
    
    if (!sheetName) {
      return ContentService.createTextOutput(JSON.stringify({
        success: false, 
        error: "ไม่พบ Action หรือ SheetName ที่ระบุ"
      })).setMimeType(ContentService.MimeType.JSON);
    }
    
    var doc = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = doc.getSheetByName(sheetName);
    
    if (!sheet) {
      sheet = doc.insertSheet(sheetName);
      // Add headers if new
      if (sheetName === 'Users') {
        sheet.appendRow(['id', 'username', 'password', 'name', 'role', 'createdAt', 'updatedAt', 'accountType', 'affiliation', 'status']);
      } else if (sheetName === 'ST5') {
        sheet.appendRow(['id', 'uid', 'userName', 'score', 'answers', 'timestamp', 'level', 'suggestion']);
      } else if (sheetName === 'Behaviors') {
        sheet.appendRow(['id', 'targetUid', 'targetName', 'selections', 'timestamp']);
      }
    }
    
    if (action === 'GET') {
      var dataRange = sheet.getDataRange();
      var values = dataRange.getValues();
      var rows = [];
      if (values.length > 1) {
        var headers = values[0];
        for (var i = 1; i < values.length; i++) {
          if (String(values[i][0]).trim() === '') continue;
          var row = {};
          for (var j = 0; j < headers.length; j++) {
            var val = values[i][j];
            if (typeof val === 'string' && (val.startsWith('{') || val.startsWith('['))) {
              try { val = JSON.parse(val); } catch(err) {}
            }
            row[headers[j]] = val;
          }
          rows.push(row);
        }
      }
      return ContentService.createTextOutput(JSON.stringify({success: true, data: rows})).setMimeType(ContentService.MimeType.JSON);
    }
    
    if (action === 'ADD' || action === 'UPDATE') {
      var headers = sheet.getDataRange().getValues()[0] || [];
      var missingHeaders = [];
      for (var key in data) {
        if (headers.indexOf(key) === -1) {
          missingHeaders.push(key);
        }
      }
      if (missingHeaders.length > 0) {
        sheet.getRange(1, headers.length + 1, 1, missingHeaders.length).setValues([missingHeaders]);
        headers = headers.concat(missingHeaders);
      }
      
      var dataRange = sheet.getDataRange();
      var values = dataRange.getValues();
      var foundRow = -1;
      
      if (data.id) {
        for (var i = 1; i < values.length; i++) {
          if (String(values[i][headers.indexOf('id')]) === String(data.id)) {
            foundRow = i + 1;
            break;
          }
        }
      }
      
      if (foundRow !== -1) {
        for (var key in data) {
          var colIndex = headers.indexOf(key);
          if (colIndex !== -1) {
            var val = data[key];
            sheet.getRange(foundRow, colIndex + 1).setValue(typeof val === 'object' ? JSON.stringify(val) : val);
          }
        }
      } else {
        var rowData = [];
        for (var i = 0; i < headers.length; i++) {
          var val = data[headers[i]];
          rowData.push(val !== undefined ? (typeof val === 'object' ? JSON.stringify(val) : val) : "");
        }
        sheet.appendRow(rowData);
      }
      
      return ContentService.createTextOutput(JSON.stringify({success: true})).setMimeType(ContentService.MimeType.JSON);
    }
    
    if (action === 'DELETE') {
      var id = data.id;
      var dataRange = sheet.getDataRange();
      var values = dataRange.getValues();
      var headers = values[0] || [];
      
      for (var i = 1; i < values.length; i++) {
        if (String(values[i][headers.indexOf('id')]) === String(id)) {
          sheet.deleteRow(i + 1);
          break;
        }
      }
      return ContentService.createTextOutput(JSON.stringify({success: true})).setMimeType(ContentService.MimeType.JSON);
    }

    return ContentService.createTextOutput(JSON.stringify({
      success: false, 
      error: "ไม่พบ Action ที่ระบุ (" + action + ")"
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      success: false, 
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  try {
    var action = e.parameter.action;
    
    if (action === 'sync') {
      var doc = SpreadsheetApp.getActiveSpreadsheet();
      var sheet = doc.getSheetByName('Users');
      var users = [];
      if (sheet) {
        var dataRange = sheet.getDataRange();
        var values = dataRange.getValues();
        if (values.length > 1) {
          var headers = values[0];
          for (var i = 1; i < values.length; i++) {
            if (String(values[i][0]).trim() === '') continue;
            var row = {};
            for (var j = 0; j < headers.length; j++) {
              row[headers[j]] = values[i][j];
            }
            users.push(row);
          }
        }
      }
      return ContentService.createTextOutput(JSON.stringify({success: true, users: users})).setMimeType(ContentService.MimeType.JSON);
    }
    
    return ContentService.createTextOutput("Mental Care API is running!").setMimeType(ContentService.MimeType.TEXT);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({success: false, error: err.toString()})).setMimeType(ContentService.MimeType.JSON);
  }
}
