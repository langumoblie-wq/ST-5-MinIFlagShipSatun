import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix key warning at 4027 (React.Fragment key={visitNum})
# visitNum is unique inside the map, but if we map over affiliations, it's safer to use `${affil}-${visitNum}`.

old_code_1 = """                                        <React.Fragment key={visitNum}>"""
new_code_1 = """                                        <React.Fragment key={`${affil}-${visitNum}`}>"""

content = content.replace(old_code_1, new_code_1)

# Check for `idx` as keys in demographic map (line 5037 etc.)
old_code_2 = """                        <div key={idx} className="flex gap-3 items-start bg-slate-50 p-4 rounded-xl border border-slate-200 break-inside-avoid shadow-sm">"""
new_code_2 = """                        <div key={`pdf-demo-${idx}`} className="flex gap-3 items-start bg-slate-50 p-4 rounded-xl border border-slate-200 break-inside-avoid shadow-sm">"""

content = content.replace(old_code_2, new_code_2)

old_code_3 = """                        <div key={idx} className="bg-slate-50 p-5 rounded-xl border border-slate-200 shadow-sm break-inside-avoid">"""
new_code_3 = """                        <div key={`pdf-rec-${idx}`} className="bg-slate-50 p-5 rounded-xl border border-slate-200 shadow-sm break-inside-avoid">"""

content = content.replace(old_code_3, new_code_3)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
