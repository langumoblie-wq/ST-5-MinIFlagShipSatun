import sys

with open('src/lib/gasDb.ts', 'r') as f:
    content = f.read()

old_msg = "if (!result.success) throw new Error(result.error);"
new_msg = "if (!result.success) throw new Error(`Google Apps Script Error: ${result.error || 'Unknown Error'}. โปรดตรวจสอบว่าได้อัปเดตโค้ดใน Apps Script ล่าสุดและ Deploy เป็น New deployment แล้ว`);"

content = content.replace(old_msg, new_msg)

with open('src/lib/gasDb.ts', 'w') as f:
    f.write(content)
print("Patched gasDb.ts with better error message")
