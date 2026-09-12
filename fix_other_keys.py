import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix at 4928 and 4942
content = content.replace('key={idx} className="flex gap-4 items-start bg-indigo-50/50', 'key={`insight-${idx}`} className="flex gap-4 items-start bg-indigo-50/50')
content = content.replace('key={idx} className="bg-blue-50/50', 'key={`rec-${idx}`} className="bg-blue-50/50')

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
