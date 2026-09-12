import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add imports
import_old = "Brain, Gamepad2, Zap, ShieldOff, Footprints, Flame, Bot, Printer, X, Trophy, Target, Pencil, Filter, ChevronDown, ChevronUp"
import_new = "Brain, Gamepad2, Zap, ShieldOff, Footprints, Flame, Bot, Printer, X, Trophy, Target, Pencil, Filter, ChevronDown, ChevronUp, TrendingDown, Minus"
content = content.replace(import_old, import_new)

# 2. Inject intervention logic in AdminDashboard
search_logic = "  const selectedUser = users.find(u => u.id === selectedUserId);"

intervention_logic = """  const selectedUser = users.find(u => u.id === selectedUserId);

  const comparisonData = useMemo(() => {
    return filteredStudents.map(student => {
        const studentSt5 = st5Data.filter(d => d.uid === student.id || d.userId === student.id).sort((a, b) => a.timestamp - b.timestamp);
        const positiveBehaviors = behaviorData.filter(d => d.targetUid === student.id && d.selections?.desirable?.length > 0);
        
        if (studentSt5.length >= 2 && positiveBehaviors.length >= 1) {
            const preTest = studentSt5[0];
            const postTest = studentSt5[studentSt5.length - 1];
            
            return {
                student,
                preScore: parseInt(preTest.score) || 0,
                postScore: parseInt(postTest.score) || 0,
                diff: (parseInt(postTest.score) || 0) - (parseInt(preTest.score) || 0),
                interventions: positiveBehaviors.length
            };
        }
        return null;
    }).filter(Boolean);
  }, [filteredStudents, st5Data, behaviorData]);"""

content = content.replace(search_logic, intervention_logic)

# 3. Inject new empty state layout
old_empty = """        ) : (
          <div className="text-center p-8">
             <div className="w-24 h-24 bg-white rounded-full flex items-center justify-center mx-auto mb-6 shadow-sm border border-slate-100">
               <UserSquare2 size={48} className="text-slate-300" strokeWidth={1.5} />
             </div>
             <h3 className="text-xl font-black text-slate-700 mb-2">เลือกรายชื่อในความดูแล</h3>
             <p className="text-slate-500 font-medium text-sm max-w-sm mx-auto">คลิกเลือกนักเรียนหรือผู้ใช้งานจากรายชื่อด้านซ้าย เพื่อดูรายงานผลสุขภาพจิตและประวัติพฤติกรรมอย่างละเอียด</p>
          </div>
        )}"""

new_empty = """        ) : (
          <div className="p-6 lg:p-8 h-full flex flex-col items-center">
            <div className="text-center mb-8 w-full max-w-2xl">
              <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center mx-auto mb-4 shadow-sm border border-slate-100">
                <TrendingUp size={40} className="text-teal-400" strokeWidth={1.5} />
              </div>
              <h3 className="text-2xl font-black text-slate-800 mb-2">ผลสัมฤทธิ์การปรับเปลี่ยนพฤติกรรม</h3>
              <p className="text-slate-500 font-medium text-sm">ตารางเปรียบเทียบผลประเมินสุขภาพจิต (ST-5) ก่อนและหลังการทำกิจกรรมเชิงบวก (Behavioral Intervention)</p>
            </div>

            {comparisonData.length > 0 ? (
                <div className="bg-white rounded-3xl border border-slate-100 shadow-sm overflow-hidden w-full max-w-3xl flex flex-col max-h-[60vh]">
                    <div className="overflow-y-auto hide-scrollbar">
                        <table className="w-full text-left">
                            <thead className="bg-slate-50 border-b border-slate-100 sticky top-0 z-10">
                                <tr>
                                    <th className="p-4 font-bold text-slate-500 text-xs tracking-wider">ชื่อ-สกุล</th>
                                    <th className="p-4 font-bold text-slate-500 text-xs tracking-wider text-center">กิจกรรมเชิงบวก</th>
                                    <th className="p-4 font-bold text-slate-500 text-xs tracking-wider text-center">ก่อนทำกิจกรรม<br/><span className="text-[9px] font-medium text-slate-400">(ST-5 แรก)</span></th>
                                    <th className="p-4 font-bold text-slate-500 text-xs tracking-wider text-center">หลังทำกิจกรรม<br/><span className="text-[9px] font-medium text-slate-400">(ST-5 ล่าสุด)</span></th>
                                    <th className="p-4 font-bold text-slate-500 text-xs tracking-wider text-center">ผลลัพธ์</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-50">
                                {comparisonData.map((row, idx) => (
                                    <tr key={`comp-${row.student.id}-${idx}`} className="hover:bg-slate-50/50 transition">
                                        <td className="p-4 text-sm font-bold text-slate-700">
                                            <button onClick={() => setSelectedUserId(row.student.id)} className="hover:text-purple-600 transition flex items-center gap-2">
                                                {row.student.name} <ChevronRight size={14} className="text-slate-300" />
                                            </button>
                                        </td>
                                        <td className="p-4 text-center">
                                            <span className="bg-teal-50 text-teal-600 px-2.5 py-1 rounded-lg text-xs font-bold border border-teal-100">{row.interventions} ครั้ง</span>
                                        </td>
                                        <td className="p-4 text-center font-black text-slate-600">{row.preScore}</td>
                                        <td className="p-4 text-center font-black text-slate-800">{row.postScore}</td>
                                        <td className="p-4 text-center">
                                            {row.diff < 0 ? (
                                                <span className="text-teal-500 font-bold flex items-center justify-center gap-1 text-sm bg-teal-50 px-2 py-1 rounded-lg border border-teal-100 w-max mx-auto"><TrendingDown size={14}/> ลดลง {Math.abs(row.diff)}</span>
                                            ) : row.diff > 0 ? (
                                                <span className="text-rose-500 font-bold flex items-center justify-center gap-1 text-sm bg-rose-50 px-2 py-1 rounded-lg border border-rose-100 w-max mx-auto"><TrendingUp size={14}/> เพิ่ม {row.diff}</span>
                                            ) : (
                                                <span className="text-slate-400 font-bold flex items-center justify-center gap-1 text-sm bg-slate-50 px-2 py-1 rounded-lg border border-slate-200 w-max mx-auto"><Minus size={14}/> คงที่</span>
                                            )}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            ) : (
                <div className="bg-white p-8 rounded-3xl border border-dashed border-slate-200 text-center w-full max-w-2xl">
                    <Activity className="mx-auto text-slate-300 mb-4" size={48} />
                    <p className="text-slate-500 font-medium mb-2">ยังไม่มีข้อมูลเปรียบเทียบผลสัมฤทธิ์</p>
                    <p className="text-slate-400 text-sm max-w-sm mx-auto leading-relaxed">ระบบจะแสดงผลเมื่อนักเรียนมีการประเมิน ST-5 อย่างน้อย 2 ครั้ง และมีการบันทึกพฤติกรรมเชิงบวกสำเร็จ</p>
                </div>
            )}
          </div>
        )}"""

content = content.replace(old_empty, new_empty)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
