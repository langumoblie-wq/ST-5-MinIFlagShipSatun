import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace the <div className="mb-8"> inside the expanded row.
# First, let's find the exact block to replace.

old_expanded_start = """                                              <div className="mb-8">
                                                  <h5 className="flex items-center gap-2 text-[13px] font-black text-slate-700 mb-4">
                                                      <Activity size={16} className="text-blue-500" /> แยกตามรายการครั้งที่ (Visits Breakdown) - ประเมินสุขภาพจิต (ST-5)
                                                  </h5>"""

old_expanded_end = """                                                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                      {Object.keys(stats.behavior.breakdown).sort((a,b)=>Number(a)-Number(b)).map(visitNum => {
                                                          const count = stats.behavior.breakdown[visitNum];
                                                          const pct = stats.target > 0 ? ((count / stats.target) * 100).toFixed(1) : '0';
                                                          return (
                                                              <div key={visitNum} className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                                                                  <div className="flex justify-between items-center mb-3 border-b border-slate-50 pb-2">
                                                                      <span className="font-bold text-[13px] text-slate-700">ครั้งที่ {visitNum}</span>
                                                                      <span className="font-black text-indigo-600 text-sm">{count} คน <span className="text-[10px] text-slate-400 font-medium ml-1">({pct}%)</span></span>
                                                                  </div>
                                                                  <div className="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                                                                      <div className="bg-indigo-500 h-full rounded-full transition-all duration-1000" style={{ width: `${Math.min(100, Number(pct))}%` }}></div>
                                                                  </div>
                                                              </div>
                                                          )
                                                      })}
                                                      {Object.keys(stats.behavior.breakdown).length === 0 && (
                                                          <div className="col-span-full text-sm text-slate-400 italic bg-white p-4 rounded-xl border border-slate-200 shadow-sm">ไม่มีข้อมูลการคัดกรองพฤติกรรม</div>
                                                      )}
                                                  </div>
                                              </div>"""

# Wait, let's just use regex to replace everything from `<div className="mb-8">` up to `</div>` (the one closing `mb-8`).
