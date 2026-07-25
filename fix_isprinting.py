import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("{(isExpanded || window.matchMedia(\"print\").matches) && (", "{(isExpanded || isPrinting) && (")

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("Fixed isPrinting")
