import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find("function ExecutiveSummaryReport")
end_idx = content.find("function AdminScreen", start_idx)
if end_idx == -1:
    end_idx = content.find("export default function App()", start_idx)

print(content[start_idx:end_idx])
