import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

start = "function ImportDashboard({ triggerAlert, triggerConfirm, profile }) {"
parts = content.split(start)
if len(parts) > 1:
    body = parts[1].split("// SUPERADMIN DASHBOARD")[0]
    with open('import_dashboard.txt', 'w') as out:
        out.write(start + body)
