import re
with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find("function ST5Form")
print(content[idx:idx+1500])
