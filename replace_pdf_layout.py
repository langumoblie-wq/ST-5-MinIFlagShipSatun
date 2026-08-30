import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# We want to replace everything from `<div ref={printRef}` to the closing `</div>` of `printRef`
start_tag = """        <div ref={printRef} className="w-[794px] bg-white print-container p-12 text-slate-800 flex flex-col space-y-8 box-border" style={{ fontFamily: 'Kanit, sans-serif' }}>"""

# Find start of the old print layout
start_idx = content.find(start_tag)
if start_idx == -1:
    print("Could not find start tag")
    exit(1)

# Find the end of it (it ends with "เอกสารฉบับนี้จัดทำโดยระบบอัตโนมัติ สำหรับใช้เป็นข้อมูลประกอบการตัดสินใจระดับบริหาร" inside a div, then closing div)
end_tag = """           <div className="text-center text-xs text-slate-400 pt-6 mt-8 border-t border-slate-100 shrink-0">
              เอกสารฉบับนี้จัดทำโดยระบบอัตโนมัติ สำหรับใช้เป็นข้อมูลประกอบการตัดสินใจระดับบริหาร
           </div>

        </div>"""

end_idx = content.find(end_tag, start_idx) + len(end_tag)

if end_idx == -1 + len(end_tag):
    print("Could not find end tag")
    exit(1)

new_layout = """        <div ref={printRef} className="w-[794px] flex flex-col">
            
           {/* PAGE 1: KPIs & Mental */}
           <div className="w-[794px] min-h-[1123px] bg-white print-container p-12 text-slate-800 flex flex-col box-border" style={{ fontFamily: 'Kanit, sans-serif' }}>
               <div className="text-center space-y-1.5 border-b-2 border-slate-800 pb-4 mb-8 shrink-0">
                  <h1 className="text-2xl font-black text-slate-900 tracking-wide">รายงานสรุปผลสัมฤทธิ์ทางการประเมินผู้บริหาร</h1>
                  <p className="text-lg font-bold text-slate-600">โครงการพัฒนาทักษะชีวิตและสุขภาพจิตเยาวชน</p>
                  <p className="text-xs text-slate-500 font-medium">ข้อมูลประมวลผล ณ วันที่ {new Date().toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
               </div>
               
               <div className="space-y-4 shrink-0 flex-grow">
                 <h2 className="text-xl font-black text-pink-700 flex items-center gap-2 border-l-4 border-pink-500 pl-3 mb-6">สรุปภาพรวม (KPIs) และ สุขภาพจิต (Mental)</h2>
                 {renderKPIs(true)}
               </div>

               <div className="mt-auto pt-6 border-t border-slate-100 shrink-0 text-center text-xs text-slate-400">
                  เอกสารฉบับนี้จัดทำโดยระบบอัตโนมัติ สำหรับใช้เป็นข้อมูลประกอบการตัดสินใจระดับบริหาร (หน้า 1/4)
               </div>
           </div>

           {/* PAGE 2: Behavior */}
           <div className="w-[794px] min-h-[1123px] bg-white print-container p-12 text-slate-800 flex flex-col box-border" style={{ fontFamily: 'Kanit, sans-serif' }}>
               <div className="text-center space-y-1.5 border-b-2 border-slate-800 pb-4 mb-8 shrink-0">
                  <h1 className="text-2xl font-black text-slate-900 tracking-wide">รายงานสรุปผลสัมฤทธิ์ทางการประเมินผู้บริหาร</h1>
                  <p className="text-lg font-bold text-slate-600">โครงการพัฒนาทักษะชีวิตและสุขภาพจิตเยาวชน</p>
                  <p className="text-xs text-slate-500 font-medium">ข้อมูลประมวลผล ณ วันที่ {new Date().toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
               </div>
               
               <div className="space-y-4 shrink-0 flex-grow">
                 <h2 className="text-xl font-black text-emerald-700 flex items-center gap-2 border-l-4 border-emerald-500 pl-3 mb-6">รายงานข้อมูลพฤติกรรม (Behavior)</h2>
                 {renderBehavior(true)}
               </div>

               <div className="mt-auto pt-6 border-t border-slate-100 shrink-0 text-center text-xs text-slate-400">
                  เอกสารฉบับนี้จัดทำโดยระบบอัตโนมัติ สำหรับใช้เป็นข้อมูลประกอบการตัดสินใจระดับบริหาร (หน้า 2/4)
               </div>
           </div>

           {/* PAGE 3: Table (Summary by Affiliation) */}
           <div className="w-[794px] min-h-[1123px] bg-white print-container p-12 text-slate-800 flex flex-col box-border" style={{ fontFamily: 'Kanit, sans-serif' }}>
               <div className="text-center space-y-1.5 border-b-2 border-slate-800 pb-4 mb-8 shrink-0">
                  <h1 className="text-2xl font-black text-slate-900 tracking-wide">รายงานสรุปผลสัมฤทธิ์ทางการประเมินผู้บริหาร</h1>
                  <p className="text-lg font-bold text-slate-600">โครงการพัฒนาทักษะชีวิตและสุขภาพจิตเยาวชน</p>
                  <p className="text-xs text-slate-500 font-medium">ข้อมูลประมวลผล ณ วันที่ {new Date().toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
               </div>
               
               <div className="space-y-4 shrink-0 flex-grow">
                 <h2 className="text-xl font-black text-blue-700 flex items-center gap-2 border-l-4 border-blue-500 pl-3 mb-6">สถิติแยกตามหน่วยงาน (สรุปยอด)</h2>
                 {renderTable(true)}
               </div>

               <div className="mt-auto pt-6 border-t border-slate-100 shrink-0 text-center text-xs text-slate-400">
                  เอกสารฉบับนี้จัดทำโดยระบบอัตโนมัติ สำหรับใช้เป็นข้อมูลประกอบการตัดสินใจระดับบริหาร (หน้า 3/4)
               </div>
           </div>

           {/* PAGE 4: Policy & AI Analysis */}
           <div className="w-[794px] min-h-[1123px] bg-white print-container p-12 text-slate-800 flex flex-col box-border" style={{ fontFamily: 'Kanit, sans-serif' }}>
               <div className="text-center space-y-1.5 border-b-2 border-slate-800 pb-4 mb-8 shrink-0">
                  <h1 className="text-2xl font-black text-slate-900 tracking-wide">รายงานสรุปผลสัมฤทธิ์ทางการประเมินผู้บริหาร</h1>
                  <p className="text-lg font-bold text-slate-600">โครงการพัฒนาทักษะชีวิตและสุขภาพจิตเยาวชน</p>
                  <p className="text-xs text-slate-500 font-medium">ข้อมูลประมวลผล ณ วันที่ {new Date().toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
               </div>
               
               <div className="space-y-6 shrink-0 flex-grow">
                 <h2 className="text-xl font-black text-indigo-700 flex items-center gap-2 border-l-4 border-indigo-500 pl-3 mb-6">บทวิเคราะห์แนวโน้ม และข้อเสนอแนะสำหรับผู้บริหาร</h2>
                 
                 <h3 className="font-bold text-slate-700 mt-4">บทวิเคราะห์ AI เชิงลึกรายประเด็น</h3>
                 <div className="grid grid-cols-1 gap-3 mb-6">
                     {aiInsightTexts.map((text, idx) => (
                        <div key={idx} className="flex gap-3 items-start bg-slate-50 p-4 rounded-xl border border-slate-200 break-inside-avoid shadow-sm">
                           <div className="w-6 h-6 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center font-bold shrink-0 text-xs">{idx + 1}</div>
                           <p className="text-slate-700 text-xs leading-relaxed pt-1">{text}</p>
                        </div>
                     ))}
                 </div>

                 <h3 className="font-bold text-slate-700 mt-6">ข้อเสนอแนะนโยบายสำหรับผู้บริหาร</h3>
                 <div className="grid grid-cols-1 gap-4">
                     {recommendations.map((rec, idx) => (
                        <div key={idx} className="bg-slate-50 p-5 rounded-xl border border-slate-200 shadow-sm break-inside-avoid">
                           <h4 className="font-bold text-slate-800 text-sm mb-1">{rec.title}</h4>
                           <p className="text-slate-600 text-[12px] leading-relaxed">{rec.text}</p>
                        </div>
                     ))}
                 </div>
               </div>
               
               <div className="mt-auto pt-6 border-t border-slate-100 shrink-0 text-center text-xs text-slate-400">
                  เอกสารฉบับนี้จัดทำโดยระบบอัตโนมัติ สำหรับใช้เป็นข้อมูลประกอบการตัดสินใจระดับบริหาร (หน้า 4/4)
               </div>
           </div>

        </div>"""

content = content[:start_idx] + new_layout + content[end_idx:]

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Replaced PDF pages!")
