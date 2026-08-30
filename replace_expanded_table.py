import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to replace lines 3866 to 3914 (the <div className="mb-8"> block)
# Let's extract the exact text using python
lines = content.split('\n')
start_index = next(i for i, line in enumerate(lines) if '<div className="mb-8">' in line)
end_index = next(i for i, line in enumerate(lines[start_index:]) if '</div>' in line and lines[start_index+i].strip() == '</div>') + start_index

# Let's verify end_index is the closing tag for mb-8.
# Actually, the block has many </div>. We can rely on line numbers roughly, but it's safer to use regex.
import ast

def find_block(text, start_marker):
    idx = text.find(start_marker)
    if idx == -1: return None, None
    depth = 0
    i = idx
    while i < len(text):
        if text[i:i+4] == '<div':
            depth += 1
        elif text[i:i+5] == '</div':
            depth -= 1
            if depth == 0:
                return idx, i+6
        i += 1
    return None, None

start, end = find_block(content, '<div className="mb-8">')
if start is not None and end is not None:
    old_block = content[start:end]
    
    new_block = """<div className="mb-8">
                                                  <h5 className="flex items-center gap-2 text-[13px] font-black text-slate-700 mb-4">
                                                      <Activity size={16} className="text-blue-500" /> สรุปผลงานตามรายการครั้งที่ (Visits Breakdown)
                                                  </h5>
                                                  <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
                                                      <table className="w-full text-left text-sm">
                                                          <thead className="bg-slate-50 border-b border-slate-100">
                                                              <tr>
                                                                  <th className="p-3 font-bold text-slate-500 text-[11px] uppercase tracking-wider text-center">ครั้งที่</th>
                                                                  <th className="p-3 font-bold text-slate-500 text-[11px] uppercase tracking-wider text-center">เป้าหมาย (คน)</th>
                                                                  <th className="p-3 font-bold text-slate-500 text-[11px] uppercase tracking-wider text-center">ผลงานรวม (คน)</th>
                                                                  <th className="p-3 font-bold text-slate-500 text-[11px] uppercase tracking-wider text-center">ร้อยละ</th>
                                                              </tr>
                                                          </thead>
                                                          <tbody className="divide-y divide-slate-100">
                                                              {Object.keys(stats.visitsBreakdown).sort((a,b)=>Number(a)-Number(b)).map(visitNum => {
                                                                  const count = stats.visitsBreakdown[visitNum];
                                                                  const pct = stats.target > 0 ? ((count / stats.target) * 100).toFixed(1) : '0';
                                                                  return (
                                                                      <tr key={visitNum} className="hover:bg-slate-50/50">
                                                                          <td className="p-3 font-bold text-slate-700 text-center">{visitNum}</td>
                                                                          <td className="p-3 text-center text-slate-600 font-medium">{stats.target}</td>
                                                                          <td className="p-3 text-center">
                                                                              <span className="font-black text-blue-600">{count}</span>
                                                                          </td>
                                                                          <td className="p-3 text-center text-teal-600 font-bold">{pct}%</td>
                                                                      </tr>
                                                                  )
                                                              })}
                                                              {Object.keys(stats.visitsBreakdown).length === 0 && (
                                                                  <tr>
                                                                      <td colSpan={4} className="p-4 text-center text-slate-400 italic text-xs">ไม่มีข้อมูลการคัดกรอง</td>
                                                                  </tr>
                                                              )}
                                                          </tbody>
                                                      </table>
                                                  </div>
                                              </div>"""
    
    content = content.replace(old_block, new_block)
    
    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced!")
else:
    print("Block not found")

