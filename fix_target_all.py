import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('const target = 50;', "const target = affil === 'all' ? 50 * (affiliations.length || 1) : 50;")

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
