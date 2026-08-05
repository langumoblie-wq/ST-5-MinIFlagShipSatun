import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Fix how error is displayed in login
old_login_error = "if (err.message && err.message.includes('Invalid credentials')) {"
new_login_error = "addLog(`Login Error: ${err.message}`, 'error');\n          setLoginError(err.message || 'รหัสผ่านไม่ถูกต้อง หรือเข้าสู่ระบบไม่สำเร็จ');\n          if (err.message && err.message.includes('Invalid credentials')) {"

if old_login_error in content:
    content = content.replace(old_login_error, new_login_error)
    print("Found and replaced login error logic")

with open('src/App.tsx', 'w') as f:
    f.write(content)

