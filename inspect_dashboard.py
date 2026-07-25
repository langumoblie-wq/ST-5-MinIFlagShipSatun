import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

start = "function ProjectReportDashboard("
end = "return ("

parts = content.split(start)
if len(parts) > 1:
    body = parts[1].split(end)[0]
    print(start + body + "return (")
