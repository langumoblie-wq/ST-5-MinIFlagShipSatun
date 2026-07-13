import re

with open('src/App.tsx', 'r') as f:
    code = f.read()

old_code = """  const [showBehaviorForm, setShowBehaviorForm] = useState(false);
  const [editingBehavior, setEditingBehavior] = useState(null);
  const [editingBehavior, setEditingBehavior] = useState(null);"""

new_code = """  const [showBehaviorForm, setShowBehaviorForm] = useState(false);
  const [editingBehavior, setEditingBehavior] = useState(null);"""

code = code.replace(old_code, new_code)

with open('src/App.tsx', 'w') as f:
    f.write(code)
print("Fixed duplicated useState!")
