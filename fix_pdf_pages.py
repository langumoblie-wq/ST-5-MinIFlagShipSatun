import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_print_layout = """      <div className="fixed top-[9999px] left-[9999px] w-[794px] pointer-events-none z-[-100]">
        <div ref={printRef} className="w-[794px] bg-white p-12 text-slate-800 space-y-10 print-container" style={{ fontFamily: 'Kanit, sans-serif' }}>
           
           {/* Document Header */}
           <div className="text-center space-y-3 border-b-2 border-slate-800 pb-6">
              <h1 className="text-3xl font-black text-slate-900 tracking-wide">รายงานสรุปผลสัมฤทธิ์ทางการประเมินผู้บริหาร</h1>
              <p className="text-xl font-bold text-slate-600">โครงการพัฒนาทักษะชีวิตและสุขภาพจิตเยาวชน</p>
              <p className="text-sm text-slate-500 font-medium">ข้อมูลประมวลผล ณ วันที่ {new Date().toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
           </div>

           {/* Section 1: KPI */}
           <div className="space-y-4">
             <h2 className="text-xl font-black text-pink-700 flex items-center gap-2 border-l-4 border-pink-500 pl-3">สรุปภาพรวม (KPIs)</h2>
             {renderKPIs(true)}
           </div>

           <div className="my-8 border-t border-slate-200"></div>

           {/* Section 2: Table Data */}
           <div className="space-y-4">
             <h2 className="text-xl font-black text-blue-700 flex items-center gap-2 border-l-4 border-blue-500 pl-3">สถิติแยกตามหน่วยงาน (สุขภาพจิต)</h2>
             {renderTable(true)}
           </div>

           <div className="my-8 border-t border-slate-200"></div>

           {/* Section 3: AI Policy */}
           <div className="space-y-6 pb-10">
             <h2 className="text-xl font-black text-indigo-700 flex items-center gap-2 border-l-4 border-indigo-500 pl-3">วิเคราะห์แนวโน้ม และข้อเสนอแนะสำหรับผู้บริหาร</h2>
             <div className="grid grid-cols-1 gap-4">
                 {recommendations.map((rec, idx) => (
                    <div key={idx} className="bg-slate-50 p-5 rounded-xl border border-slate-200">
                       <h4 className="font-bold text-slate-800 text-base mb-1">{rec.title}</h4>
                       <p className="text-slate-600 text-sm leading-relaxed">{rec.text}</p>
                    </div>
                 ))}
             </div>
           </div>
           
           {/* Footer Page */}
           <div className="text-center text-xs text-slate-400 mt-10 pt-4 border-t border-slate-100">
              เอกสารฉบับนี้จัดทำโดยระบบอัตโนมัติ สำหรับใช้เป็นข้อมูลประกอบการตัดสินใจระดับบริหาร
           </div>

        </div>
      </div>"""

new_print_layout = """      <div className="fixed top-[9999px] left-[9999px] w-[794px] pointer-events-none z-[-100]">
        <div ref={printRef} className="w-[794px] bg-white print-container flex flex-col" style={{ fontFamily: 'Kanit, sans-serif' }}>
           
           {/* PAGE 1 */}
           <div className="w-[794px] h-[1122px] bg-white p-12 text-slate-800 flex flex-col box-border">
               <div className="text-center space-y-3 border-b-2 border-slate-800 pb-6 mb-8 shrink-0">
                  <h1 className="text-3xl font-black text-slate-900 tracking-wide">รายงานสรุปผลสัมฤทธิ์ทางการประเมินผู้บริหาร</h1>
                  <p className="text-xl font-bold text-slate-600">โครงการพัฒนาทักษะชีวิตและสุขภาพจิตเยาวชน</p>
                  <p className="text-sm text-slate-500 font-medium">ข้อมูลประมวลผล ณ วันที่ {new Date().toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
               </div>
               
               <div className="space-y-4 mb-8 shrink-0">
                 <h2 className="text-xl font-black text-pink-700 flex items-center gap-2 border-l-4 border-pink-500 pl-3">สรุปภาพรวม (KPIs)</h2>
                 {renderKPIs(true)}
               </div>

               <div className="space-y-4 flex-1 overflow-hidden">
                 <h2 className="text-xl font-black text-blue-700 flex items-center gap-2 border-l-4 border-blue-500 pl-3">สถิติแยกตามหน่วยงาน (สุขภาพจิต)</h2>
                 {renderTable(true)}
               </div>
               
               <div className="text-right text-xs text-slate-400 pt-4 mt-4 border-t border-slate-100 shrink-0">
                  หน้า 1/2
               </div>
           </div>

           {/* PAGE 2 */}
           <div className="w-[794px] h-[1122px] bg-white p-12 text-slate-800 flex flex-col box-border">
               <div className="space-y-6 flex-1 shrink-0">
                 <h2 className="text-xl font-black text-indigo-700 flex items-center gap-2 border-l-4 border-indigo-500 pl-3">วิเคราะห์แนวโน้ม และข้อเสนอแนะสำหรับผู้บริหาร</h2>
                 <div className="grid grid-cols-1 gap-4">
                     {recommendations.map((rec, idx) => (
                        <div key={idx} className="bg-slate-50 p-5 rounded-xl border border-slate-200 shadow-sm">
                           <h4 className="font-bold text-slate-800 text-base mb-1">{rec.title}</h4>
                           <p className="text-slate-600 text-[13px] leading-relaxed">{rec.text}</p>
                        </div>
                     ))}
                 </div>
               </div>
               
               <div className="text-center text-xs text-slate-400 mt-auto pt-4 border-t border-slate-100 shrink-0">
                  เอกสารฉบับนี้จัดทำโดยระบบอัตโนมัติ สำหรับใช้เป็นข้อมูลประกอบการตัดสินใจระดับบริหาร<br/>หน้า 2/2
               </div>
           </div>

        </div>
      </div>"""

if old_print_layout in content:
    content = content.replace(old_print_layout, new_print_layout)
    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced!")
else:
    print("Not found")

