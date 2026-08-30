import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Web UI replacement
search_ui = """                 <h3 className="text-lg font-black text-indigo-800 flex items-center gap-2 border-b border-indigo-100 pb-3">
                   <Bot size={24} /> บทวิเคราะห์ AI เชิงลึกรายประเด็น
                 </h3>"""

replace_ui = """                 <h3 className="text-lg font-black text-indigo-800 flex items-center gap-2 border-b border-indigo-100 pb-3">
                   <Users size={24} /> บทวิเคราะห์ความสัมพันธ์ (เพศ/อายุ)
                 </h3>
                 <div className="space-y-4">
                   {demoData.insights.map((text, idx) => (
                      <div key={`demo-${idx}`} className="flex gap-4 items-start bg-indigo-50/50 p-5 rounded-2xl border border-indigo-100">
                         <div className="w-8 h-8 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center font-bold shrink-0">{idx + 1}</div>
                         <p className="text-slate-700 text-sm leading-relaxed pt-1.5">{text}</p>
                      </div>
                   ))}
                 </div>
                 
                 <h3 className="text-lg font-black text-indigo-800 flex items-center gap-2 border-b border-indigo-100 pb-3 mt-6">
                   <Bot size={24} /> บทวิเคราะห์ AI เชิงลึกรายประเด็น
                 </h3>"""

if search_ui in content:
    content = content.replace(search_ui, replace_ui)
    print("Injected web UI")
else:
    print("Could not find web UI")

# PDF replacement
search_pdf = """                 <h3 className="font-bold text-slate-700 mt-4">บทวิเคราะห์ AI เชิงลึกรายประเด็น</h3>"""

replace_pdf = """                 <h3 className="font-bold text-slate-700 mt-4">บทวิเคราะห์ความสัมพันธ์ประชากรศาสตร์ (เพศ และ อายุ)</h3>
                 <div className="grid grid-cols-1 gap-3 mb-6">
                     {demoData.insights.map((text, idx) => (
                        <div key={`demo-${idx}`} className="flex gap-3 items-start bg-slate-50 p-4 rounded-xl border border-slate-200 break-inside-avoid shadow-sm">
                           <div className="w-6 h-6 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center font-bold shrink-0 text-xs">{idx + 1}</div>
                           <p className="text-slate-700 text-xs leading-relaxed pt-1">{text}</p>
                        </div>
                     ))}
                 </div>

                 <h3 className="font-bold text-slate-700 mt-4">บทวิเคราะห์ AI เชิงลึกรายประเด็น</h3>"""

if search_pdf in content:
    content = content.replace(search_pdf, replace_pdf)
    print("Injected PDF UI")
else:
    print("Could not find PDF UI")

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
