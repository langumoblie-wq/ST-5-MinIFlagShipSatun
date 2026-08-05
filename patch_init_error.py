import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Fix how error is displayed in login
old_login_error = "console.error(\"Init error:\", error);"
new_login_error = "console.error(\"Init error:\", error);\n        setError(error.message || 'เกิดข้อผิดพลาดในการเริ่มต้นระบบ');"

if old_login_error in content:
    content = content.replace(old_login_error, new_login_error)
    print("Found and replaced init error logic")

with open('src/App.tsx', 'w') as f:
    f.write(content)

