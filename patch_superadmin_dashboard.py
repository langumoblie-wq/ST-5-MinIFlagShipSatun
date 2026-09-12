import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add comparisonData memoization logic
search_logic = "  const pendingAdmins = displayUsers.filter(u => u.role === 'admin' && u.status === 'pending');"

intervention_logic = """  const pendingAdmins = displayUsers.filter(u => u.role === 'admin' && u.status === 'pending');

  const comparisonData = useMemo(() => {
    const students = displayUsers.filter(u => ['student', 'community', 'teacher'].includes(u.accountType));
    return students.map(student => {
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
  }, [displayUsers, st5Data, behaviorData]);"""

content = content.replace(search_logic, intervention_logic)

# 2. Add the UI block between Pending Admins and Manage all users
search_ui = """      <div className="bg-white p-6 md:p-8 rounded-[2.5rem] shadow-sm border border-slate-100">
        <h3 className="font-black text-xl mb-6 text-slate-800">จัดการผู้ใช้งานทั้งหมดในระบบ</h3>"""

new_ui = """      <div className="bg-white p-6 md:p-8 rounded-[2.5rem] shadow-sm border border-slate-100">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-12 h-12 bg-teal-50 rounded-2xl flex items-center justify-center border border-teal-100">
            <TrendingUp size={24} className="text-teal-500" strokeWidth={2.5} />
          </div>
          <div>
            <h3 className="font-black text-xl text-slate-800">ผลสัมฤทธิ์การปรับเปลี่ยนพฤติกรรม</h3>
            <p className="text-slate-500 font-medium text-xs">เปรียบเทียบผลประเมิน ST-5 ก่อนและหลังทำกิจกรรมเชิงบวก</p>
          </div>
        </div>

        {comparisonData.length > 0 ? (
            <div className="bg-white rounded-3xl border border-slate-100 shadow-sm overflow-hidden w-full max-h-[50vh] flex flex-col">
                <div className="overflow-y-auto hide-scrollbar">
                    <table className="w-full text-left">
                        <thead className="bg-slate-50 border-b border-slate-100 sticky top-0 z-10">
                            <tr>
                                <th className="p-4 font-bold text-slate-500 text-xs tracking-wider">ชื่อ-สกุล / สังกัด</th>
                                <th className="p-4 font-bold text-slate-500 text-xs tracking-wider text-center">กิจกรรมเชิงบวก</th>
                                <th className="p-4 font-bold text-slate-500 text-xs tracking-wider text-center">ก่อนทำกิจกรรม<br/><span className="text-[9px] font-medium text-slate-400">(ST-5 แรก)</span></th>
                                <th className="p-4 font-bold text-slate-500 text-xs tracking-wider text-center">หลังทำกิจกรรม<br/><span className="text-[9px] font-medium text-slate-400">(ST-5 ล่าสุด)</span></th>
                                <th className="p-4 font-bold text-slate-500 text-xs tracking-wider text-center">ผลลัพธ์</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-50">
                            {comparisonData.map((row, idx) => (
                                <tr key={`sup-comp-${row.student.id}-${idx}`} className="hover:bg-slate-50/50 transition">
                                    <td className="p-4 text-sm font-bold text-slate-700">
                                        {row.student.name}
                                        <div className="text-[10px] text-slate-400 mt-1">{row.student.affiliation}</div>
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
            <div className="bg-slate-50 p-6 rounded-3xl border border-dashed border-slate-200 text-center">
                <Activity className="mx-auto text-slate-300 mb-3" size={32} />
                <p className="text-slate-500 font-medium text-sm">ยังไม่มีข้อมูลเปรียบเทียบผลสัมฤทธิ์ในสังกัดนี้</p>
            </div>
        )}
      </div>

      <div className="bg-white p-6 md:p-8 rounded-[2.5rem] shadow-sm border border-slate-100">
        <h3 className="font-black text-xl mb-6 text-slate-800">จัดการผู้ใช้งานทั้งหมดในระบบ</h3>"""

content = content.replace(search_ui, new_ui)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
