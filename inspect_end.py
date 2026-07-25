import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

start = "function ProjectReportDashboard("
parts = content.split(start)
if len(parts) > 1:
    body = parts[1].split("// --- App Component ---")[0]
    lines = body.split("\n")
    print("\n".join(lines[-20:]))
