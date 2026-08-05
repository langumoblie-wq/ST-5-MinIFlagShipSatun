import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Fix how error is displayed in login
old_login_error = "setError(err.message || 'เกิดข้อผิดพลาดในการเชื่อมต่อ');"
new_login_error = "addLog(`Login Error: ${err.message}`, 'error');\n      setError(err.message || 'เกิดข้อผิดพลาดในการเชื่อมต่อ');"

if old_login_error in content:
    content = content.replace(old_login_error, new_login_error)
    print("Found and replaced login error logic")

with open('src/App.tsx', 'w') as f:
    f.write(content)

