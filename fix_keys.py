import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix repeatStudents st5
content = re.sub(
    r'stats\.st5\.repeatStudents\.map\(\(student\)\s*=>\s*\(\s*<tr key=\{student\.id\}',
    r'stats.st5.repeatStudents.map((student, idx) => (\n                                                                      <tr key={`st5-rep-${student.id}-${idx}`}',
    content
)

# Fix repeatStudents behavior
content = re.sub(
    r'stats\.behavior\.repeatStudents\.map\(\(student\)\s*=>\s*\(\s*<tr key=\{student\.id\}',
    r'stats.behavior.repeatStudents.map((student, idx) => (\n                                                                      <tr key={`beh-rep-${student.id}-${idx}`}',
    content
)

# Fix desItems and undItems
content = re.sub(
    r'desItems\.map\(\(k\)\s*=>\s*<li key=\{k\}',
    r'desItems.map((k, idx) => <li key={`des-${idx}-${k}`}',
    content
)
content = re.sub(
    r'undItems\.map\(\(k\)\s*=>\s*<li key=\{k\}',
    r'undItems.map((k, idx) => <li key={`und-${idx}-${k}`}',
    content
)

# Fix admin and users in filteredStudents
content = re.sub(
    r'filteredStudents\.map\(\(student,\s*index\)\s*=>\s*\{\s*return\s*\(\s*<div key=\{student\.id\}',
    r'filteredStudents.map((student, index) => {\n            return (\n              <div key={`student-${student.id}-${index}`}',
    content
)

# Fix Admin rendering
content = re.sub(
    r'pendingAdmins\.map\(admin\s*=>\s*\(\s*<li key=\{admin\.id\}',
    r'pendingAdmins.map((admin, idx) => (\n              <li key={`admin-${admin.id}-${idx}`}',
    content
)
content = re.sub(
    r'roleUsers\.map\(u\s*=>\s*\(\s*<tr key=\{u\.id\}',
    r'roleUsers.map((u, idx) => (\n                      <tr key={`roleu-${u.id}-${idx}`}',
    content
)

# Fix history items
content = re.sub(
    r'st5History\.map\(\(item,\s*idx\)\s*=>\s*\{\s*return\s*\(\s*<div key=\{item\.id\}',
    r'st5History.map((item, idx) => {\n              return (\n                <div key={`st5hist-${item.id || idx}-${idx}`}',
    content
)
content = re.sub(
    r'behaviorHistory\.map\(\(item,\s*idx\)\s*=>\s*\{\s*return\s*\(\s*<div key=\{item\.id\}',
    r'behaviorHistory.map((item, idx) => {\n              return (\n                <div key={`behist-${item.id || idx}-${idx}`}',
    content
)
content = re.sub(
    r'return uSt5\.map\(\(item:\s*any,\s*idx:\s*number\)\s*=>\s*\{\s*return\s*\(\s*<div key=\{item\.id\}',
    r'return uSt5.map((item: any, idx: number) => {\n                      return (\n                        <div key={`ust5-${item.id || idx}-${idx}`}',
    content
)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
