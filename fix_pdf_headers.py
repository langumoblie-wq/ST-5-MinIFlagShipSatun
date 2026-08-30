import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_header = """               <div className="text-center space-y-3 border-b-2 border-slate-800 pb-6 mb-8 shrink-0">
                  <h1 className="text-3xl font-black text-slate-900 tracking-wide">รายงานสรุปผลสัมฤทธิ์ทางการประเมินผู้บริหาร</h1>
                  <p className="text-xl font-bold text-slate-600">โครงการพัฒนาทักษะชีวิตและสุขภาพจิตเยาวชน</p>
                  <p className="text-sm text-slate-500 font-medium">ข้อมูลประมวลผล ณ วันที่ {new Date().toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
               </div>"""

new_header = """               <div className="text-center space-y-1.5 border-b-2 border-slate-800 pb-4 mb-6 shrink-0">
                  <h1 className="text-2xl font-black text-slate-900 tracking-wide">รายงานสรุปผลสัมฤทธิ์ทางการประเมินผู้บริหาร</h1>
                  <p className="text-lg font-bold text-slate-600">โครงการพัฒนาทักษะชีวิตและสุขภาพจิตเยาวชน</p>
                  <p className="text-xs text-slate-500 font-medium">ข้อมูลประมวลผล ณ วันที่ {new Date().toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
               </div>"""

if old_header in content:
    content = content.replace(old_header, new_header)
    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced Header!")
else:
    print("Header Not found")

