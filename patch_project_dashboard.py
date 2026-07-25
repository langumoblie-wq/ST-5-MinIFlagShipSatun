import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Check imports
import_target = "import { \n  Users, ShieldCheck,"
if "Trophy" not in content and import_target in content:
    content = content.replace("Bot, Printer, X,", "Bot, Printer, X, Trophy, ChevronDown, ChevronUp, Pencil,")
elif "Trophy" not in content:
    content = content.replace("import {", "import { Trophy, ChevronDown, ChevronUp, Pencil,", 1)

# Replace ProjectReportDashboard
start_marker = "function ProjectReportDashboard({ users, st5Data, behaviorData, profile }) {"
end_marker = "function ST5Form({ onSubmit, onCancel, initialData }) {"

parts = content.split(start_marker)
if len(parts) == 2:
    subparts = parts[1].split(end_marker)
    if len(subparts) == 2:
        new_component = """
  const [targets, setTargets] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('project_targets')) || {};
    } catch {
      return {};
    }
  });
  const [globalTarget, setGlobalTarget] = useState(() => {
    return parseInt(localStorage.getItem('project_global_target')) || 1000;
  });
  const [selectedAffiliation, setSelectedAffiliation] = useState('all');
  const [expandedRows, setExpandedRows] = useState({});
  const [editingTarget, setEditingTarget] = useState(null);

  useEffect(() => {
    localStorage.setItem('project_targets', JSON.stringify(targets));
  }, [targets]);

  useEffect(() => {
    localStorage.setItem('project_global_target', globalTarget.toString());
  }, [globalTarget]);

  const affiliations = Array.from(new Set(users.filter(u => u.accountType === 'student').map(u => u.affiliation).filter(Boolean)));
  
  const getStats = (affil) => {
    let studentsInAffil = users.filter(u => u.accountType === 'student');
    if (affil !== 'all') {
      studentsInAffil = studentsInAffil.filter(u => u.affiliation === affil);
    }
    
    const userVisits = {};
    const st5InAffil = st5Data.filter(d => studentsInAffil.some(u => u.id === (d.uid || d.userId)));
    
    st5InAffil.forEach(d => {
      const id = d.uid || d.userId;
      if (!userVisits[id]) userVisits[id] = [];
      userVisits[id].push(d);
    });

    const uniqueScreenedCount = Object.keys(userVisits).length;
    const totalVisitsCount = st5InAffil.length;
    
    const visitsBreakdown = {};
    Object.values(userVisits).forEach(visits => {
        const count = visits.length;
        for (let i = 1; i <= count; i++) {
            if (!visitsBreakdown[i]) visitsBreakdown[i] = 0;
            visitsBreakdown[i]++;
        }
    });

    const repeatScreenedStudents = studentsInAffil
        .filter(u => (userVisits[u.id]?.length || 0) > 1)
        .map(u => ({
            ...u,
            times: userVisits[u.id].length,
            visits: userVisits[u.id].sort((a,b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
        }))
        .sort((a, b) => b.times - a.times);

    const target = affil === 'all' ? globalTarget : (targets[affil] || 100);
    const progressPercent = target > 0 ? ((uniqueScreenedCount / target) * 100).toFixed(1) : 0;

    return {
        uniqueScreenedCount,
        totalVisitsCount,
        target,
        progressPercent,
        visitsBreakdown,
        repeatScreenedStudents
    };
  };

  const overviewStats = getStats(selectedAffiliation);

  const toggleRow = (affil) => {
      setExpandedRows(prev => ({ ...prev, [affil]: !prev[affil] }));
  };

  const handleSaveTarget = (affil, value) => {
      if (affil === 'all') {
          setGlobalTarget(Number(value));
      } else {
          setTargets(prev => ({ ...prev, [affil]: Number(value) }));
      }
      setEditingTarget(null);
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="space-y-6 print-container animate-in fade-in duration-500 bg-slate-50/50 min-h-screen p-2 md:p-4 rounded-3xl">
      
      <div className="bg-white p-6 md:p-8 rounded-[2rem] shadow-sm border border-slate-100 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div className="flex gap-4 items-start">
           <div className="text-blue-600 mt-1">
             <Trophy size={32} strokeWidth={2} />
           </div>
           <div>
             <h2 className="text-xl md:text-2xl font-black text-slate-800">สรุปผลและการติดตามโครงการ</h2>
             <p className="text-xs md:text-sm text-slate-500 font-medium mt-1">ติดตามความก้าวหน้าการคัดกรองแยกตามโมเดลและพื้นที่เป้าหมาย</p>
           </div>
        </div>

        <div className="flex flex-col md:flex-row items-stretch md:items-center gap-4 w-full md:w-auto">
          <button onClick={handlePrint} className="bg-slate-50 hover:bg-slate-100 text-slate-700 border border-slate-200 px-4 py-2.5 rounded-xl font-bold flex items-center justify-center gap-2 transition shadow-sm text-sm no-print">
            <Printer size={16} /> พิมพ์รายงาน
          </button>
          
          <div className="flex gap-3 w-full md:w-auto">
              <div className="bg-slate-50 px-5 py-3 rounded-2xl flex items-center gap-4 border border-slate-100 w-1/2 md:w-auto justify-between md:justify-start">
                  <div>
                      <div className="flex items-center gap-1.5 text-slate-500 text-[11px] font-bold mb-1">
                          <Users size={14} /> คัดกรองแล้ว
                      </div>
                      <div className="flex items-baseline gap-1">
                          <span className="text-2xl font-black text-slate-800">{overviewStats.uniqueScreenedCount}</span>
                          <span className="text-[10px] font-bold text-slate-500">คน</span>
                      </div>
                  </div>
                  <div className="text-[10px] text-slate-400 font-medium text-right mt-auto hidden md:block whitespace-nowrap">
                      ทั้งหมด {overviewStats.totalVisitsCount} ครั้ง (visits)
                  </div>
              </div>

              <div className="bg-emerald-50/50 px-5 py-3 rounded-2xl flex flex-col justify-center border border-emerald-100/50 w-1/2 md:w-auto">
                  <div className="flex items-center gap-1.5 text-slate-500 text-[11px] font-bold mb-1">
                      <Target size={14} /> เป้าหมายรวม
                  </div>
                  <div className="flex items-baseline gap-1">
                      {editingTarget?.id === 'all' ? (
                          <input 
                              type="number"
                              autoFocus
                              defaultValue={overviewStats.target}
                              onBlur={(e) => handleSaveTarget('all', e.target.value)}
                              onKeyDown={(e) => e.key === 'Enter' && handleSaveTarget('all', e.target.value)}
                              className="w-16 bg-white border border-slate-300 rounded px-1 font-bold text-lg outline-none focus:border-emerald-400"
                          />
                      ) : (
                          <>
                              <span className="text-2xl font-black text-slate-800">{overviewStats.target}</span>
                              <span className="text-[10px] font-bold text-slate-500">คน</span>
                              <button onClick={() => setEditingTarget({ id: 'all', value: overviewStats.target })} className="ml-1 text-slate-300 hover:text-slate-500 no-print">
                                  <Pencil size={12} />
                              </button>
                          </>
                      )}
                  </div>
                  <div className="text-[11px] text-emerald-600 font-black mt-0.5">
                      คิดเป็น {overviewStats.progressPercent}%
                  </div>
              </div>
          </div>
        </div>
      </div>

      <div className="bg-white p-4 rounded-[1.5rem] shadow-sm border border-slate-100 flex flex-col md:flex-row md:items-center gap-4 no-print">
         <div className="flex items-center gap-2 text-slate-500 font-bold text-sm px-2">
            <Filter size={16} /> ตัวกรอง:
         </div>
         <div className="flex flex-wrap gap-3">
             <select 
                value={selectedAffiliation}
                onChange={(e) => setSelectedAffiliation(e.target.value)}
                className="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-xl px-4 py-2 font-medium min-w-[200px] outline-none focus:border-blue-300 transition-colors"
             >
                <option value="all">ทุกพื้นที่เป้าหมาย / สังกัด</option>
                {affiliations.map(aff => (
                    <option key={aff} value={aff}>{aff}</option>
                ))}
             </select>
             <div className="bg-slate-50 border border-slate-200 text-slate-400 text-sm rounded-xl px-4 py-2 font-medium min-w-[150px] cursor-not-allowed flex items-center justify-between">
                ทุกโมเดล <ChevronDown size={14}/>
             </div>
             <div className="bg-slate-50 border border-slate-200 text-slate-400 text-sm rounded-xl px-4 py-2 font-medium min-w-[150px] cursor-not-allowed flex items-center justify-between">
                ทุกอำเภอ <ChevronDown size={14}/>
             </div>
         </div>
      </div>

      <div className="bg-white rounded-[2rem] shadow-sm border border-slate-100 overflow-hidden print-card">
          <div className="overflow-x-auto">
              <table className="w-full text-left">
                  <thead className="bg-slate-50/80 border-b border-slate-100 hidden md:table-header-group">
                      <tr>
                          <th className="p-5 font-bold text-slate-500 text-[11px] tracking-wider w-1/4">พื้นที่เป้าหมาย (AREA)</th>
                          <th className="p-5 font-bold text-slate-500 text-[11px] tracking-wider">โมเดล / อำเภอ</th>
                          <th className="p-5 font-bold text-slate-500 text-[11px] tracking-wider text-center">ยอดคัดกรอง (คน)</th>
                          <th className="p-5 font-bold text-slate-500 text-[11px] tracking-wider text-center">จำนวนครั้ง (VISITS)</th>
                          <th className="p-5 font-bold text-slate-500 text-[11px] tracking-wider text-center">เป้าหมาย (คน)</th>
                          <th className="p-5 font-bold text-slate-500 text-[11px] tracking-wider w-1/4">ความก้าวหน้า</th>
                      </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-50">
                      {(selectedAffiliation === 'all' ? affiliations : [selectedAffiliation]).map(affil => {
                          const stats = getStats(affil);
                          const isExpanded = expandedRows[affil];
                          
                          return (
                              <React.Fragment key={affil}>
                                  <tr className="hover:bg-slate-50/30 transition-colors group flex flex-col md:table-row">
                                      <td className="p-4 md:p-5">
                                          <button onClick={() => toggleRow(affil)} className="flex items-center gap-2 text-sm font-black text-slate-800 no-print w-full text-left">
                                              {isExpanded ? <ChevronDown size={16} className="text-slate-400" /> : <ChevronRight size={16} className="text-slate-400" />}
                                              {affil} 
                                              <span className="text-[9px] text-blue-500 font-medium bg-blue-50 px-2 py-0.5 rounded-full opacity-0 group-hover:opacity-100 transition-opacity ml-2 hidden md:inline-block">(คลิกดูรายละเอียด)</span>
                                          </button>
                                          <div className="print-only font-black text-slate-800 text-sm hidden">
                                              {affil}
                                          </div>
                                      </td>
                                      <td className="p-4 md:p-5 md:table-cell flex justify-between items-center bg-slate-50/50 md:bg-transparent">
                                          <span className="md:hidden text-[10px] font-bold text-slate-500">โมเดล / อำเภอ</span>
                                          <div className="flex flex-col items-start gap-1">
                                              <span className="text-[9px] font-black bg-indigo-50 text-indigo-600 px-2 py-0.5 rounded-full">ตำบล</span>
                                              <span className="text-xs text-slate-600 font-medium pl-1">{affil}</span>
                                          </div>
                                      </td>
                                      <td className="p-4 md:p-5 md:text-center md:table-cell flex justify-between items-center">
                                          <span className="md:hidden text-[10px] font-bold text-slate-500">ยอดคัดกรอง</span>
                                          <span className="text-lg font-black text-slate-800">{stats.uniqueScreenedCount}</span>
                                      </td>
                                      <td className="p-4 md:p-5 md:text-center md:table-cell flex justify-between items-center bg-slate-50/50 md:bg-transparent">
                                          <span className="md:hidden text-[10px] font-bold text-slate-500">จำนวนครั้ง (VISITS)</span>
                                          <span className="text-sm font-bold bg-slate-100 text-slate-600 px-3 py-1 rounded-full">{stats.totalVisitsCount}</span>
                                      </td>
                                      <td className="p-4 md:p-5 md:text-center flex justify-between md:justify-center items-center h-auto md:h-[72px] md:table-cell">
                                          <span className="md:hidden text-[10px] font-bold text-slate-500">เป้าหมาย</span>
                                          <div className="flex items-center gap-1 justify-end md:justify-center">
                                              {editingTarget?.id === affil ? (
                                                  <input 
                                                      type="number"
                                                      autoFocus
                                                      defaultValue={stats.target}
                                                      onBlur={(e) => handleSaveTarget(affil, e.target.value)}
                                                      onKeyDown={(e) => e.key === 'Enter' && handleSaveTarget(affil, e.target.value)}
                                                      className="w-16 bg-white border border-slate-300 rounded px-1 font-bold text-sm text-center outline-none focus:border-indigo-400"
                                                  />
                                              ) : (
                                                  <>
                                                      <span className="text-lg font-black text-indigo-700">{stats.target}</span>
                                                      <button onClick={() => setEditingTarget({ id: affil, value: stats.target })} className="text-slate-300 hover:text-slate-500 no-print">
                                                          <Pencil size={12} />
                                                      </button>
                                                  </>
                                              )}
                                          </div>
                                      </td>
                                      <td className="p-4 md:p-5 md:table-cell flex flex-col justify-center bg-slate-50/50 md:bg-transparent">
                                          <div className="flex flex-col gap-1 w-full">
                                              <div className="flex justify-between items-end mb-1">
                                                  <span className="text-sm font-black text-teal-600">{stats.progressPercent}%</span>
                                                  <span className="text-[10px] text-slate-500 font-bold">{stats.uniqueScreenedCount} / {stats.target}</span>
                                              </div>
                                              <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
                                                  <div className="bg-teal-500 h-full rounded-full transition-all duration-1000" style={{ width: `${Math.min(100, Number(stats.progressPercent))}%` }}></div>
                                              </div>
                                          </div>
                                      </td>
                                  </tr>
                                  
                                  {(isExpanded || window.matchMedia("print").matches) && (
                                      <tr className="bg-slate-50/30 print-row-expanded border-t border-slate-100">
                                          <td colSpan={6} className="p-4 md:p-8 border-b border-slate-100">
                                              
                                              <div className="mb-8">
                                                  <h5 className="flex items-center gap-2 text-[13px] font-black text-slate-700 mb-4">
                                                      <Activity size={16} className="text-blue-500" /> แยกตามรายการครั้งที่ (Visits Breakdown)
                                                  </h5>
                                                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                      {Object.keys(stats.visitsBreakdown).sort((a,b)=>Number(a)-Number(b)).map(visitNum => {
                                                          const count = stats.visitsBreakdown[visitNum];
                                                          const pct = stats.target > 0 ? ((count / stats.target) * 100).toFixed(1) : 0;
                                                          return (
                                                              <div key={visitNum} className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                                                                  <div className="flex justify-between items-center mb-3 border-b border-slate-50 pb-2">
                                                                      <span className="font-bold text-[13px] text-slate-700">ครั้งที่ {visitNum}</span>
                                                                      <span className="text-[13px] font-black text-blue-700">{count} คน</span>
                                                                  </div>
                                                                  <div className="flex justify-between items-end mb-1.5">
                                                                      <span className="text-[10px] text-slate-500 font-medium">ความก้าวหน้า ({count}/{stats.target})</span>
                                                                      <span className="text-[11px] font-black text-blue-600">{pct}%</span>
                                                                  </div>
                                                                  <div className="w-full bg-indigo-100/50 h-1.5 rounded-full overflow-hidden">
                                                                      <div className="bg-indigo-500 h-full rounded-full transition-all duration-1000" style={{ width: `${Math.min(100, Number(pct))}%` }}></div>
                                                                  </div>
                                                              </div>
                                                          )
                                                      })}
                                                      {Object.keys(stats.visitsBreakdown).length === 0 && (
                                                          <div className="col-span-full text-sm text-slate-400 italic bg-white p-4 rounded-xl border border-slate-200 shadow-sm">ไม่มีข้อมูลการคัดกรอง</div>
                                                      )}
                                                  </div>
                                              </div>

                                              <div>
                                                  <h5 className="flex items-center gap-2 text-[13px] font-black text-slate-700 mb-4">
                                                      <Users size={16} className="text-orange-500" /> รายการซ้ำ / รับบริการหลายครั้ง ({stats.repeatScreenedStudents.length} รายการ)
                                                  </h5>
                                                  {stats.repeatScreenedStudents.length > 0 ? (
                                                      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm">
                                                          <table className="w-full text-left text-sm">
                                                              <thead className="bg-slate-50 border-b border-slate-100">
                                                                  <tr>
                                                                      <th className="p-3 font-bold text-slate-500 text-[11px] uppercase tracking-wider">ชื่อ-สกุล</th>
                                                                      <th className="p-3 font-bold text-slate-500 text-[11px] uppercase tracking-wider text-center w-24 md:w-32">จำนวนครั้ง</th>
                                                                      <th className="p-3 font-bold text-slate-500 text-[11px] uppercase tracking-wider hidden md:table-cell">รายการครั้งที่ (Visits)</th>
                                                                  </tr>
                                                              </thead>
                                                              <tbody className="divide-y divide-slate-50">
                                                                  {stats.repeatScreenedStudents.map((student) => (
                                                                      <tr key={student.id} className="hover:bg-slate-50/50">
                                                                          <td className="p-3 font-bold text-slate-700 text-xs">{student.name}</td>
                                                                          <td className="p-3 text-center">
                                                                              <span className="font-black text-orange-600 text-[13px]">{student.times}</span>
                                                                          </td>
                                                                          <td className="p-3 hidden md:table-cell">
                                                                              <div className="flex flex-wrap gap-1">
                                                                                  {student.visits.map((v, idx) => (
                                                                                      <span key={idx} className="bg-slate-100 text-slate-600 px-2 py-0.5 rounded text-[9px] font-medium border border-slate-200">
                                                                                          ครั้งที่ {idx + 1}
                                                                                      </span>
                                                                                  ))}
                                                                              </div>
                                                                          </td>
                                                                      </tr>
                                                                  ))}
                                                              </tbody>
                                                          </table>
                                                      </div>
                                                  ) : (
                                                      <div className="text-[13px] text-slate-400 italic bg-white p-4 rounded-xl border border-slate-200 shadow-sm">ไม่พบผู้รับบริการหลายครั้ง</div>
                                                  )}
                                              </div>

                                          </td>
                                      </tr>
                                  )}
                              </React.Fragment>
                          )
                      })}
                      {affiliations.length === 0 && (
                          <tr>
                              <td colSpan={6} className="p-8 text-center text-slate-400 font-medium">ไม่พบข้อมูลสังกัดในระบบ</td>
                          </tr>
                      )}
                  </tbody>
              </table>
          </div>
      </div>
    </div>
  );
}
"""
        new_content = parts[0] + start_marker + new_component + end_marker + subparts[1]
        with open('src/App.tsx', 'w') as f:
            f.write(new_content)
        print("Patched successfully")
    else:
        print("End marker not found")
else:
    print("Start marker not found")

