import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_print = """      {/* ---------------------------------------------------------
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
             <h2 className="text-xl font-black text-pink-700 flex items-center gap-2 border-l-4 border-pink-500 pl-3">สรุปภาพรวม (KPIs) และ สุขภาพจิต (Mental)</h2>
             {renderKPIs(true)}
           </div>
           
           <div className="space-y-4 shrink-0 pt-2">
             <h2 className="text-xl font-black text-emerald-700 flex items-center gap-2 border-l-4 border-emerald-500 pl-3">รายงานข้อมูลพฤติกรรม (Behavior)</h2>
             {renderBehavior(true)}
           </div>

           <div className="space-y-4 shrink-0 pt-2">
             <h2 className="text-xl font-black text-blue-700 flex items-center gap-2 border-l-4 border-blue-500 pl-3">สถิติแยกตามหน่วยงาน (สรุปยอด)</h2>
             {renderTable(true)}
           </div>

           <div className="space-y-6 shrink-0 pt-4 border-t border-slate-200">
             <h2 className="text-xl font-black text-indigo-700 flex items-center gap-2 border-l-4 border-indigo-500 pl-3">บทวิเคราะห์แนวโน้ม และข้อเสนอแนะสำหรับผู้บริหาร</h2>
             
             <h3 className="font-bold text-slate-700 mt-4">บทวิเคราะห์ AI เชิงลึกรายประเด็น</h3>
             <div className="grid grid-cols-1 gap-3 mb-6">
                 {aiInsightTexts.map((text, idx) => (
                    <div key={idx} className="flex gap-3 items-start bg-slate-50 p-4 rounded-xl border border-slate-200 break-inside-avoid shadow-sm">
                       <div className="w-6 h-6 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center font-bold shrink-0 text-xs">{idx + 1}</div>
                       <p className="text-slate-700 text-xs leading-relaxed pt-1">{text}</p>
                    </div>
                 ))}
             </div>

             <h3 className="font-bold text-slate-700">ข้อเสนอแนะนโยบายสำหรับผู้บริหาร</h3>
             <div className="grid grid-cols-1 gap-4">
                 {recommendations.map((rec, idx) => (
                    <div key={idx} className="bg-slate-50 p-5 rounded-xl border border-slate-200 shadow-sm break-inside-avoid">
                       <h4 className="font-bold text-slate-800 text-sm mb-1">{rec.title}</h4>
                       <p className="text-slate-600 text-[12px] leading-relaxed">{rec.text}</p>
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
    print("Replaced PDF Layout!")
else:
    print("Not found PDF Layout!")

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
