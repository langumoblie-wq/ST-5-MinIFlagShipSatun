import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

old_code = """const data = JSON.parse(evt.target.result);"""
new_code = """const data = JSON.parse(evt.target.result as string);"""

if old_code in content:
    content = content.replace(old_code, new_code)
else:
    print("Could not find old_code")

with open('src/App.tsx', 'w') as f:
    f.write(content)
