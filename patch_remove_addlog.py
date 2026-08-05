import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("addLog(`Init Error: ${error.message}`, 'error');\n        ", "")
content = content.replace("addLog(`Login Error: ${err.message}`, 'error');\n      ", "")

with open('src/App.tsx', 'w') as f:
    f.write(content)
print("Removed addLog")
