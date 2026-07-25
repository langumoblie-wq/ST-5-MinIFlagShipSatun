import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("return True;", "return true;")

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("Fixed True to true")
