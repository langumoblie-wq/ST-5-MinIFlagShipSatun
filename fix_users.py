import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix ProjectReportDashboard
content = content.replace("users.filter(u => u.accountType === 'student')", "users.filter(u => ['student', 'community'].includes(u.accountType) || u.role === 'user')")

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
