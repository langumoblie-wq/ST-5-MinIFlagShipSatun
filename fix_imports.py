import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("Bot, Printer, X", "Bot, Printer, X, Trophy, Target, Pencil, Filter, ChevronDown, ChevronUp")

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("Imports fixed")
