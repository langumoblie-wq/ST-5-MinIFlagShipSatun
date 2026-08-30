import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

search_tab_behavior = """         {reportTab === 'behavior' && (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500 text-center py-10">
               <ShieldCheck size={48} className="mx-auto text-emerald-300 mb-4" />
               <h3 className="text-xl font-bold text-slate-700">รายงานข้อมูลพฤติกรรม</h3>
               <p className="text-slate-500">รวบรวมข้อมูลพฤติกรรมเชิงบวก และ พฤติกรรมที่ต้องเฝ้าระวังเพื่อใช้ในการวิเคราะห์ต่อไป</p>
            </div>
         )}"""

insertion_tab_behavior = """         {reportTab === 'behavior' && (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
               {renderBehavior()}
            </div>
         )}"""

content = content.replace(search_tab_behavior, insertion_tab_behavior)

search_tab_policy = """         {reportTab === 'policy' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <h3 className="text-lg font-black text-indigo-800 flex items-center gap-2 border-b border-indigo-100 pb-3">
                 <Bot size={24} /> บทวิเคราะห์แนวโน้ม และข้อเสนอแนะ
               </h3>
               <div className="space-y-4">
                 {recommendations.map((rec, idx) => (
                    <div key={idx} className="bg-indigo-50/50 p-5 rounded-2xl border border-indigo-100">
                       <h4 className="font-bold text-indigo-700 mb-2">{rec.title}</h4>
                       <p className="text-slate-700 text-sm leading-relaxed">{rec.text}</p>
                    </div>
                 ))}
               </div>
            </div>
         )}"""

insertion_tab_policy = """         {reportTab === 'policy' && (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <div className="space-y-6">
                 <h3 className="text-lg font-black text-indigo-800 flex items-center gap-2 border-b border-indigo-100 pb-3">
                   <Bot size={24} /> บทวิเคราะห์ AI เชิงลึกรายประเด็น
                 </h3>
                 <div className="space-y-4">
                   {aiInsightTexts.map((text, idx) => (
                      <div key={idx} className="flex gap-4 items-start bg-indigo-50/50 p-5 rounded-2xl border border-indigo-100">
                         <div className="w-8 h-8 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center font-bold shrink-0">{idx + 1}</div>
                         <p className="text-slate-700 text-sm leading-relaxed pt-1.5">{text}</p>
                      </div>
                   ))}
                 </div>
               </div>

               <div className="space-y-6">
                 <h3 className="text-lg font-black text-blue-800 flex items-center gap-2 border-b border-blue-100 pb-3">
                   <Lightbulb size={24} /> ข้อเสนอแนะนโยบายสำหรับผู้บริหาร
                 </h3>
                 <div className="space-y-4">
                   {recommendations.map((rec, idx) => (
                      <div key={idx} className="bg-blue-50/50 p-5 rounded-2xl border border-blue-100">
                         <h4 className="font-bold text-blue-700 mb-2">{rec.title}</h4>
                         <p className="text-slate-700 text-sm leading-relaxed">{rec.text}</p>
                      </div>
                   ))}
                 </div>
               </div>
            </div>
         )}"""

content = content.replace(search_tab_policy, insertion_tab_policy)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
