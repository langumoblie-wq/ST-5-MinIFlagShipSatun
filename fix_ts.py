import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix riskPercentage fallback
content = content.replace("toFixed(1) : 0;", "toFixed(1) : '0';")

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
