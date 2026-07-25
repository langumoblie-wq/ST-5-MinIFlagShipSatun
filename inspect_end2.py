import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

start = "function ProjectReportDashboard("
end = "function ST5Form("
parts = content.split(start)
if len(parts) > 1:
    body = parts[1].split(end)[0]
    lines = body.split("\n")
    print("\n".join(lines[-20:]))
