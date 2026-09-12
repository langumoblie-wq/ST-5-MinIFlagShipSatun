import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old1 = """{recentSt5.map((item) => {"""
new1 = """{recentSt5.map((item, idx) => {"""
content = content.replace(old1, new1)

old2 = """<div key={item.id} className="p-4 border border-slate-100 rounded-2xl bg-slate-50/50 flex justify-between items-center gap-3">"""
new2 = """<div key={`${item.id}-${idx}`} className="p-4 border border-slate-100 rounded-2xl bg-slate-50/50 flex justify-between items-center gap-3">"""
content = content.replace(old2, new2)

old3 = """{recentBeh.map((item, idx) => {"""
new3 = """{recentBeh.map((item, idx) => {"""
content = content.replace(old3, new3)

old4 = """<div key={item.id || idx} className="p-4 border border-slate-100 rounded-2xl bg-slate-50/50 flex justify-between items-center gap-3">"""
new4 = """<div key={`beh-${item.id}-${idx}`} className="p-4 border border-slate-100 rounded-2xl bg-slate-50/50 flex justify-between items-center gap-3">"""
content = content.replace(old4, new4)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
