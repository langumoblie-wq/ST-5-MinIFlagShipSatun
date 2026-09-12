import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace key={student.id} with key={`${student.id}-${index}`}
old1 = """<div key={student.id} onClick={() => setSelectedUserId(student.id)}"""
new1 = """<div key={`${student.id}-${index}`} onClick={() => setSelectedUserId(student.id)}"""
content = content.replace(old1, new1)

# SuperAdmin lists users
# Need to check other key={u.id}
# In ProjectReportDashboard:
old2 = """{studentsInAffiliation.map(u => <option key={u.id} value={u.id}>{u.name} (@{u.id})</option>)}"""
new2 = """{studentsInAffiliation.map((u, index) => <option key={`${u.id}-${index}`} value={u.id}>{u.name} (@{u.id})</option>)}"""
content = content.replace(old2, new2)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
