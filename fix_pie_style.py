import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove fill: '#475569' from style={{...}}
content = content.replace("style={{fontSize: '11px', fontWeight: 'bold', fill: '#475569'}}", "style={{fontSize: '11px', fontWeight: 'bold'}}")

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
