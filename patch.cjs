const fs = require('fs');
let code = fs.readFileSync('src/App.tsx', 'utf8');

code = code.replace(/\/\/ Upload to Google Drive via Apps Script([\s\S]*?)setSuccess\('สร้างบัญชีและบันทึก PDF ลง Google Drive สำเร็จ!'\);/m, 
`// Upload to Google Drive via Apps Script
      await gasRequest('UPLOAD_PDF', 'Users', { filename: filename, base64: pdfBase64 });
      
      setSuccess('สร้างบัญชีและบันทึก PDF ลง Google Drive สำเร็จ!');`);

fs.writeFileSync('src/App.tsx', code);
