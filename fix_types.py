import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("const userVisits = {};", "const userVisits: Record<string, any[]> = {};")

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("Types fixed")
