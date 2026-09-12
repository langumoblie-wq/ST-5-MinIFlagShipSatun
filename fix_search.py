import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_code = """  // ค้นหา
  const filteredStudents = students.filter(u => 
    u.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
    (u.id && u.id.toLowerCase().includes(searchQuery.toLowerCase()))
  );"""

new_code = """  // ค้นหา
  const filteredStudents = students.filter(u => 
    (u.name && String(u.name).toLowerCase().includes(searchQuery.toLowerCase())) || 
    (u.id && String(u.id).toLowerCase().includes(searchQuery.toLowerCase()))
  );"""

if old_code in content:
    content = content.replace(old_code, new_code)
    print("Fixed AdminDashboard search logic")
else:
    print("Could not find AdminDashboard search logic")

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
