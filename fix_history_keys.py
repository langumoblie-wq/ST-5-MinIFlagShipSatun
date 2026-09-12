import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix in AdminStudentDetail
old1 = """{st5History.map((item) => ("""
new1 = """{st5History.map((item, index) => ("""
content = content.replace(old1, new1)

old2 = """<div key={item.id} className="p-5 md:p-6 border border-slate-100 rounded-[2rem] bg-slate-50/50 space-y-4">"""
new2 = """<div key={`${item.id}-${index}`} className="p-5 md:p-6 border border-slate-100 rounded-[2rem] bg-slate-50/50 space-y-4">"""
content = content.replace(old2, new2)

old3 = """{behaviorHistory.map((item) => ("""
new3 = """{behaviorHistory.map((item, index) => ("""
content = content.replace(old3, new3)

old4 = """<div key={item.id} className="p-5 md:p-6 border border-slate-100 rounded-[2rem] bg-white shadow-sm hover:shadow-md transition space-y-4">"""
new4 = """<div key={`${item.id}-${index}`} className="p-5 md:p-6 border border-slate-100 rounded-[2rem] bg-white shadow-sm hover:shadow-md transition space-y-4">"""
content = content.replace(old4, new4)

# In BehaviorForm
old5 = """{st5History.map(st5 => ("""
new5 = """{st5History.map((st5, index) => ("""
content = content.replace(old5, new5)

old6 = """<option key={st5.id} value={st5.id}>"""
new6 = """<option key={`${st5.id}-${index}`} value={st5.id}>"""
content = content.replace(old6, new6)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
