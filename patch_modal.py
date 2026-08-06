import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

new_modal = """
    {/* Restore Progress Modal */}
    {restoreStatus && restoreStatus.isRestoring && (
        <div className="fixed inset-0 z-[200] flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-in fade-in">
           <div className="bg-white p-6 md:p-8 rounded-[2rem] max-w-md w-full shadow-2xl border border-slate-100 text-center space-y-5 animate-in zoom-in-95">
              <div className="mx-auto w-16 h-16 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center shadow-inner border-2 border-white mb-2">
                 {restoreStatus.finished ? (
                     restoreStatus.error ? <AlertCircle size={32} className="text-red-600" /> : <CheckCircle2 size={32} />
                 ) : (
                     <Database size={32} className="animate-pulse" />
                 )}
              </div>
              <h3 className="text-xl font-black text-slate-800">
                  {restoreStatus.finished ? (restoreStatus.error ? 'เกิดข้อผิดพลาด' : 'กู้คืนข้อมูลสำเร็จ') : 'กำลังกู้คืนข้อมูล...'}
              </h3>
              <p className={`text-sm ${restoreStatus.error ? 'text-red-600' : 'text-slate-600'}`}>
                  {restoreStatus.message}
              </p>
              
              {!restoreStatus.finished && restoreStatus.total > 0 && (
                  <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden mt-4">
                      <div 
                          className="bg-indigo-500 h-full rounded-full transition-all duration-300" 
                          style={{ width: `${Math.min(100, (restoreStatus.current / restoreStatus.total) * 100)}%` }}
                      ></div>
                  </div>
              )}

              {restoreStatus.finished && (
                  <div className="pt-2">
                     <button 
                        onClick={() => setRestoreStatus(null)}
                        className="w-full py-4 bg-slate-800 text-white font-bold rounded-xl hover:bg-slate-700 shadow-md transition"
                     >
                        ปิดหน้าต่าง
                     </button>
                  </div>
              )}
           </div>
        </div>
    )}
    </>
  );
}"""

content = content.replace("    </>\n  );\n}", new_modal)

with open('src/App.tsx', 'w') as f:
    f.write(content)
print("Patch applied")
