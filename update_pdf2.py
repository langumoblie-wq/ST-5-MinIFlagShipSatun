import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_canvas = """      const canvas = await toPng(element, { 
          quality: 1.0, 
          backgroundColor: '#ffffff', 
          pixelRatio: 2,
          width: 794
      });"""

content = content.replace(old_canvas, "")

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
