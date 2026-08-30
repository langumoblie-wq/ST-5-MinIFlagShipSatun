import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_print = """      {/* ---------------------------------------------------------
          HIDDEN PRINTABLE VIEW (A4 Optimized layout for PDF) 
          --------------------------------------------------------- */}
      <div className="fixed top-[9999px] left-[9999px] w-[794px] pointer-events-none z-[-100]">
        <div ref={printRef} className="w-[794px] bg-white print-container flex flex-col" style={{ fontFamily: 'Kanit, sans-serif' }}>
           
           {/* PAGE 1 */}
           <div className="w-[794px] h-[1122px] bg-white p-12 text-slate-800 flex flex-col box-border">
               <div className="text-center space-y-1.5 border-b-2 border-slate-800 pb-4 mb-6 shrink-0">
                  <h1 className="text-2xl font-black text-slate-900 tracking-wide">รายงานสรุปผลสัมฤทธิ์ทางการประเมินผู้บริหาร</h1>
                  <p className="text-lg font-bold text-slate-600">โครงการพัฒนาทักษะชีวิตและสุขภาพจิตเยาวชน</p>
                  <p className="text-xs text-slate-500 font-medium">ข้อมูลประมวลผล ณ วันที่ {new Date().toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
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

new_print = """      {/* ---------------------------------------------------------
          HIDDEN PRINTABLE VIEW (Continuous layout for PDF Export) 
          --------------------------------------------------------- */}
      <div className="fixed top-[9999px] left-[9999px] w-[794px] pointer-events-none z-[-100]">
        <div ref={printRef} className="w-[794px] bg-white print-container p-12 text-slate-800 flex flex-col space-y-8 box-border" style={{ fontFamily: 'Kanit, sans-serif' }}>
           
           <div className="text-center space-y-1.5 border-b-2 border-slate-800 pb-4 mb-2 shrink-0">
              <h1 className="text-2xl font-black text-slate-900 tracking-wide">รายงานสรุปผลสัมฤทธิ์ทางการประเมินผู้บริหาร</h1>
              <p className="text-lg font-bold text-slate-600">โครงการพัฒนาทักษะชีวิตและสุขภาพจิตเยาวชน</p>
              <p className="text-xs text-slate-500 font-medium">ข้อมูลประมวลผล ณ วันที่ {new Date().toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
           </div>
           
           <div className="space-y-4 shrink-0">
             <h2 className="text-xl font-black text-pink-700 flex items-center gap-2 border-l-4 border-pink-500 pl-3">สรุปภาพรวม (KPIs)</h2>
             {renderKPIs(true)}
           </div>

           <div className="space-y-4 shrink-0">
             <h2 className="text-xl font-black text-blue-700 flex items-center gap-2 border-l-4 border-blue-500 pl-3">สถิติแยกตามหน่วยงาน (สุขภาพจิต)</h2>
             {renderTable(true)}
           </div>
           
           <div className="space-y-6 shrink-0 pt-4 border-t border-slate-200">
             <h2 className="text-xl font-black text-indigo-700 flex items-center gap-2 border-l-4 border-indigo-500 pl-3">วิเคราะห์แนวโน้ม และข้อเสนอแนะสำหรับผู้บริหาร</h2>
             <div className="grid grid-cols-1 gap-4">
                 {recommendations.map((rec, idx) => (
                    <div key={idx} className="bg-slate-50 p-5 rounded-xl border border-slate-200 shadow-sm break-inside-avoid">
                       <h4 className="font-bold text-slate-800 text-base mb-1">{rec.title}</h4>
                       <p className="text-slate-600 text-[13px] leading-relaxed">{rec.text}</p>
                    </div>
                 ))}
             </div>
           </div>
           
           <div className="text-center text-xs text-slate-400 pt-6 mt-8 border-t border-slate-100 shrink-0">
              เอกสารฉบับนี้จัดทำโดยระบบอัตโนมัติ สำหรับใช้เป็นข้อมูลประกอบการตัดสินใจระดับบริหาร
           </div>

        </div>
      </div>"""

if old_print in content:
    content = content.replace(old_print, new_print)
    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced!")
else:
    print("Not found")

