import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

component = """function ProjectReportDashboard({ users, st5Data, behaviorData, profile }) {
  const [targetCount, setTargetCount] = useState(() => {
      return parseInt(localStorage.getItem('project_target_count')) || 1000;
  });
  const [selectedAffiliation, setSelectedAffiliation] = useState(profile.role === 'superadmin' ? 'all' : profile.affiliation);

  useEffect(() => {
      localStorage.setItem('project_target_count', targetCount.toString());
  }, [targetCount]);

  const affiliations = Array.from(new Set(users.filter(u => u.accountType === 'student').map(u => u.affiliation).filter(Boolean)));
  const allStudents = users.filter(u => u.accountType === 'student');
  const uniqueScreenedUids = new Set(st5Data.map(d => d.uid || d.userId));
  
  let studentsToConsider = allStudents;
  if (selectedAffiliation !== 'all') {
      studentsToConsider = studentsToConsider.filter(u => Array.isArray(selectedAffiliation) ? selectedAffiliation.includes(u.affiliation) : u.affiliation === selectedAffiliation);
  }

  const screenedStudents = studentsToConsider.filter(u => uniqueScreenedUids.has(u.id));
  const actualScreenedCount = screenedStudents.length;
  const totalCount = studentsToConsider.length;
  const percentToTarget = targetCount > 0 ? ((actualScreenedCount / targetCount) * 100).toFixed(1) : 0;
  const percentToTotal = totalCount > 0 ? ((actualScreenedCount / totalCount) * 100).toFixed(1) : 0;

  const screeningCounts = {};
  st5Data.forEach(d => {
      const id = d.uid || d.userId;
      if (!screeningCounts[id]) screeningCounts[id] = 0;
      screeningCounts[id]++;
  });

  const repeatScreenedStudents = screenedStudents.filter(u => screeningCounts[u.id] > 1).map(u => ({
      ...u,
      times: screeningCounts[u.id]
  })).sort((a,b) => b.times - a.times);

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="space-y-6 print-container animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white p-6 rounded-3xl shadow-sm border border-slate-100 no-print hide-on-print">
        <h3 className="font-black text-2xl text-slate-800 flex items-center gap-3">
          <PieChart className="text-blue-500" size={28} /> สรุปผลและติดตามโครงการ
        </h3>
        <div className="flex items-center gap-3 flex-wrap">
          {profile.role === 'superadmin' && (
            <select 
              value={selectedAffiliation} 
              onChange={e => setSelectedAffiliation(e.target.value)}
              className="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-xl focus:ring-blue-500 focus:border-blue-500 block p-2.5 font-medium"
            >
              <option value="all">ทุกสังกัด (ภาพรวม)</option>
              {affiliations.map(aff => <option key={aff} value={aff}>{aff}</option>)}
            </select>
          )}
          <div className="flex items-center gap-2 bg-blue-50 px-3 py-2 rounded-xl border border-blue-100">
            <span className="text-xs font-bold text-blue-700 whitespace-nowrap">เป้าหมายคัดกรอง:</span>
            <input 
              type="number" 
              value={targetCount}
              onChange={(e) => setTargetCount(Number(e.target.value) || 0)}
              className="w-20 bg-white border border-blue-200 text-slate-700 text-sm rounded-lg p-1 font-bold text-center"
            />
          </div>
          <button onClick={handlePrint} className="bg-slate-800 hover:bg-slate-700 text-white px-4 py-2.5 rounded-xl font-bold flex items-center gap-2 shadow-sm transition">
            <Printer size={18} /> พิมพ์รายงาน (PDF)
          </button>
        </div>
      </div>

      <div className="hidden print-only text-center mb-6">
        <h1 className="text-2xl font-black text-slate-800">รายงานสรุปผลและติดตามโครงการ</h1>
        <p className="text-sm text-slate-500 mt-2">
          {selectedAffiliation === 'all' ? 'ภาพรวมทุกสังกัด' : `สังกัด: ${selectedAffiliation}`}
        </p>
        <p className="text-xs text-slate-400 mt-1">พิมพ์เมื่อ: {new Date().toLocaleDateString('th-TH')} เวลา {new Date().toLocaleTimeString('th-TH')}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100 flex flex-col justify-center print-card">
          <p className="text-sm font-bold text-slate-500 mb-2 uppercase tracking-wide">จำนวนคัดกรองแล้ว (คน)</p>
          <div className="flex items-end gap-2">
            <span className="text-5xl font-black text-slate-800">{actualScreenedCount}</span>
            <span className="text-sm font-bold text-slate-400 mb-1">/ {totalCount} นักเรียนในระบบ</span>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-3xl shadow-sm border border-blue-100 bg-gradient-to-br from-white to-blue-50 flex flex-col justify-center print-card">
          <p className="text-sm font-bold text-blue-500 mb-2 uppercase tracking-wide">เป้าหมายที่ตั้งไว้ (คน)</p>
          <div className="flex items-end gap-2">
            <span className="text-5xl font-black text-blue-700">{targetCount}</span>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-3xl shadow-sm border border-teal-100 bg-gradient-to-br from-white to-teal-50 flex flex-col justify-center print-card">
          <p className="text-sm font-bold text-teal-500 mb-2 uppercase tracking-wide">ความสำเร็จเทียบเป้าหมาย (%)</p>
          <div className="flex items-end gap-2">
            <span className="text-5xl font-black text-teal-700">{percentToTarget}%</span>
          </div>
          <div className="w-full bg-teal-100 h-2 mt-3 rounded-full overflow-hidden">
            <div className="bg-teal-500 h-full rounded-full transition-all duration-1000" style={{ width: `${Math.min(100, Number(percentToTarget))}%` }}></div>
          </div>
        </div>
      </div>

      <div className="bg-white p-6 md:p-8 rounded-3xl shadow-sm border border-slate-100 print-card break-inside-avoid">
        <h4 className="font-black text-lg text-slate-800 mb-4 flex items-center gap-2 pb-3 border-b border-slate-100">
          <Activity className="text-purple-500" size={20} /> รายการนักเรียนที่มีการคัดกรองซ้ำ (มากกว่า 1 ครั้ง)
          <span className="bg-purple-100 text-purple-700 px-2.5 py-0.5 rounded-full text-xs font-bold ml-2">{repeatScreenedStudents.length} คน</span>
        </h4>
        
        {repeatScreenedStudents.length > 0 ? (
          <div className="overflow-x-auto mt-4 max-h-[400px] print:max-h-none overflow-y-auto custom-scrollbar">
            <table className="w-full text-left text-sm print-table relative">
              <thead className="sticky top-0 bg-slate-50 z-10 print:static">
                <tr className="text-slate-500 border-b-2 border-slate-200">
                  <th className="p-3 font-bold text-xs uppercase tracking-wider rounded-tl-xl">ชื่อ-นามสกุล</th>
                  <th className="p-3 font-bold text-xs uppercase tracking-wider">รหัส (ID)</th>
                  <th className="p-3 font-bold text-xs uppercase tracking-wider">สังกัด</th>
                  <th className="p-3 font-bold text-xs uppercase tracking-wider text-center rounded-tr-xl">จำนวนครั้งที่คัดกรอง</th>
                </tr>
              </thead>
              <tbody>
                {repeatScreenedStudents.map((s, idx) => (
                  <tr key={s.id} className="border-b border-slate-50 hover:bg-slate-50">
                    <td className="p-3 font-bold text-slate-700">{s.name}</td>
                    <td className="p-3 text-slate-500 font-mono text-xs">{s.uid || s.id}</td>
                    <td className="p-3 text-slate-500">{s.affiliation || '-'}</td>
                    <td className="p-3 text-center">
                      <span className="bg-orange-100 text-orange-700 font-black px-3 py-1 rounded-full">{s.times} ครั้ง</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-slate-400 font-medium">ไม่พบการประเมินซ้ำในสังกัดที่เลือก</p>
          </div>
        )}
      </div>

      <div className="bg-gradient-to-br from-indigo-50 to-purple-50 p-6 md:p-8 rounded-3xl border border-indigo-100 print-card break-inside-avoid">
        <h4 className="font-black text-lg text-indigo-800 mb-3 flex items-center gap-2">
          <Sparkles className="text-indigo-500" size={20} /> ข้อเสนอแนะเพิ่มเติมจากระบบ
        </h4>
        <ul className="space-y-2 text-sm text-indigo-900/80 leading-relaxed font-medium list-disc pl-5">
          {Number(percentToTarget) < 50 && <li>อัตราการคัดกรองยังต่ำกว่า 50% ของเป้าหมาย แนะนำให้เร่งประชาสัมพันธ์หรือจัดกิจกรรมคัดกรองเชิงรุกในสถานศึกษา</li>}
          {Number(percentToTarget) >= 50 && Number(percentToTarget) < 100 && <li>การคัดกรองดำเนินไปได้ดีเกินครึ่งหนึ่งของเป้าหมาย ควรติดตามกลุ่มที่ยังตกหล่นให้ครบถ้วน</li>}
          {Number(percentToTarget) >= 100 && <li>บรรลุเป้าหมายการคัดกรองแล้ว! ยอดเยี่ยมมาก ควรให้ความสำคัญกับการติดตามนักเรียนในกลุ่มเสี่ยงสูงเป็นลำดับถัดไป</li>}
          {repeatScreenedStudents.length > 0 && <li>พบนักเรียนที่มีการประเมินซ้ำ {repeatScreenedStudents.length} คน ซึ่งแสดงถึงการเฝ้าระวังอย่างต่อเนื่อง หรืออาจมีการกรอกข้อมูลซ้ำซ้อน ควรตรวจสอบความถูกต้องของข้อมูลประเมิน</li>}
          <li>ระบบจะคำนวณจำนวนคัดกรองจากนักเรียน 1 คนต่อการประเมิน 1 หรือหลายครั้งก็นับเป็น 1 คนเท่านั้น เพื่อให้ได้ยอดที่สะท้อนบุคคลจริง</li>
        </ul>
      </div>

    </div>
  );
}

"""

target = "function ST5Form({ onSubmit, onCancel, initialData }) {"

if target in content:
    content = content.replace(target, component + "\n" + target)
    print("Component appended successfully")
else:
    print("ST5Form not found")

with open('src/App.tsx', 'w') as f:
    f.write(content)
