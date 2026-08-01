import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

new_end = """      </div>
    </div>
    
    {/* Duplicate Confirmation Modal */}
    {duplicateCheck && (
        <div className="fixed inset-0 z-[200] flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-in fade-in">
           <div className="bg-white p-6 md:p-8 rounded-[2rem] max-w-md w-full shadow-2xl border border-slate-100 text-center space-y-5 animate-in zoom-in-95">
              <div className="mx-auto w-16 h-16 bg-amber-100 text-amber-600 rounded-full flex items-center justify-center shadow-inner border-2 border-white mb-2">
                 <AlertCircle size={32} />
              </div>
              <h3 className="text-xl font-black text-slate-800">พบข้อมูลซ้ำซ้อน</h3>
              <p className="text-slate-600 text-sm">
                 ผู้ใช้: <span className="font-bold text-slate-800">{duplicateCheck.student.name}</span><br />
                 (Username: <span className="font-mono bg-slate-100 px-2 py-0.5 rounded text-slate-700">{duplicateCheck.student.username}</span>)<br />
                 มีอยู่ในระบบอยู่แล้ว คุณต้องการนำเข้าข้อมูลใหม่ไปทับข้อมูลเดิมหรือไม่?
              </p>
              <div className="flex gap-3 pt-4">
                 <button 
                    onClick={() => duplicateCheck.resolve(false)}
                    className="flex-1 py-3 bg-slate-100 text-slate-600 font-bold rounded-xl hover:bg-slate-200 transition"
                 >
                    ยกเลิก (ข้ามรายการนี้)
                 </button>
                 <button 
                    onClick={() => duplicateCheck.resolve(true)}
                    className="flex-1 py-3 bg-amber-500 text-white font-bold rounded-xl hover:bg-amber-600 shadow-md transition"
                 >
                    ยืนยัน (เขียนทับ)
                 </button>
              </div>
           </div>
        </div>
    )}

    {/* Import Summary Modal */}
    {importSummary && (
        <div className="fixed inset-0 z-[200] flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-in fade-in">
           <div className="bg-white p-6 md:p-8 rounded-[2rem] max-w-md w-full shadow-2xl border border-slate-100 text-center space-y-5 animate-in zoom-in-95">
              <div className="mx-auto w-16 h-16 bg-teal-100 text-teal-600 rounded-full flex items-center justify-center shadow-inner border-2 border-white mb-2">
                 <CheckCircle2 size={32} />
              </div>
              <h3 className="text-xl font-black text-slate-800">สรุปผลการนำเข้าข้อมูล</h3>
              
              <div className="bg-slate-50 rounded-2xl p-4 space-y-3 text-left">
                  <div className="flex justify-between items-center text-sm">
                      <span className="text-slate-500 font-medium">รายการทั้งหมด</span>
                      <span className="font-bold text-slate-800">{importSummary.total}</span>
                  </div>
                  <div className="flex justify-between items-center text-sm border-t border-slate-200 pt-3">
                      <span className="text-teal-600 font-medium">นำเข้าใหม่สำเร็จ</span>
                      <span className="font-bold text-teal-600">{importSummary.success}</span>
                  </div>
                  <div className="flex justify-between items-center text-sm border-t border-slate-200 pt-3">
                      <span className="text-amber-600 font-medium">เขียนทับสำเร็จ</span>
                      <span className="font-bold text-amber-600">{importSummary.overwritten}</span>
                  </div>
                  <div className="flex justify-between items-center text-sm border-t border-slate-200 pt-3">
                      <span className="text-slate-500 font-medium">ข้ามรายการ</span>
                      <span className="font-bold text-slate-500">{importSummary.skipped}</span>
                  </div>
              </div>

              <div className="pt-2">
                 <button 
                    onClick={() => setImportSummary(null)}
                    className="w-full py-4 bg-slate-800 text-white font-bold rounded-xl hover:bg-slate-700 shadow-md transition"
                 >
                    ปิดหน้าต่าง
                 </button>
              </div>
           </div>
        </div>
    )}
    </>
  );
}"""

old_end = """      </div>
    </div>
  );
}"""

content = content.replace(new_end, old_end)

# Now apply new_end ONLY to ImportDashboard
parts = content.split("function ImportDashboard")
if len(parts) > 1:
    body = parts[1]
    # find the first occurrence of old_end in body and replace with new_end
    body = body.replace(old_end, new_end, 1)
    content = parts[0] + "function ImportDashboard" + body
    
with open('src/App.tsx', 'w') as f:
    f.write(content)
