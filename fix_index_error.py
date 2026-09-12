import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix in AdminStudentDetail (st5History.map and behaviorHistory.map use `idx` but the key references `index`)
old1 = """<div key={`${item.id}-${index}`} className="p-5 md:p-6 border border-slate-100 rounded-[2rem] bg-slate-50/50 space-y-4">"""
new1 = """<div key={`${item.id}-${idx}`} className="p-5 md:p-6 border border-slate-100 rounded-[2rem] bg-slate-50/50 space-y-4">"""
content = content.replace(old1, new1)

old2 = """<div key={`${item.id}-${index}`} className="p-5 md:p-6 border border-slate-100 rounded-[2rem] bg-white shadow-sm hover:shadow-md transition space-y-4">"""
new2 = """<div key={`${item.id}-${idx}`} className="p-5 md:p-6 border border-slate-100 rounded-[2rem] bg-white shadow-sm hover:shadow-md transition space-y-4">"""
content = content.replace(old2, new2)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
