import sys

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
for i, line in enumerate(lines):
    if "function ExecutiveSummaryReport" in line:
        start_idx = i
        break

if start_idx == -1:
    print("Could not find ExecutiveSummaryReport")
    sys.exit(1)

# The rest of the file is this component.
lines = lines[:start_idx]

new_component = """// ==========================================
// EXECUTIVE SUMMARY REPORT - FOR SUPERADMIN
// ==========================================
function ExecutiveSummaryReport({ users, st5Data, behaviorData, profile }) {
  const [reportTab, setReportTab] = useState('kpi');
  const [isExporting, setIsExporting] = useState(false);
  const printRef = useRef(null);

  // --- Data Processing ---
  const students = users.filter(u => ['student', 'community'].includes(u.accountType));
  const totalStudents = students.length;
  const totalEvaluations = st5Data.length + behaviorData.length;
  
  // Use uid to match student id
  const st5Risk = st5Data.filter(d => ['เครียดสูง', 'เครียดรุนแรง'].includes(d.level) || parseInt(d.score) >= 8);
  const riskPercentage = totalStudents > 0 ? ((st5Risk.length / totalStudents) * 100).toFixed(1) : 0;

  const affiliations = [...new Set(students.map(u => u.affiliation).filter(Boolean))];

  // Table Data & Sorting
  const tableData = affiliations.map(aff => {
    const affStudents = students.filter(s => s.affiliation === aff);
    const affSt5 = st5Data.filter(d => affStudents.some(s => s.id === d.uid));
    const affRisk = affSt5.filter(d => ['เครียดสูง', 'เครียดรุนแรง'].includes(d.level) || parseInt(d.score) >= 8).length;
    return { name: aff, students: affStudents.length, evaluations: affSt5.length, risk: affRisk };
  }).sort((a, b) => b.students - a.students);

  // ST-5 Chart Data
  const st5Levels = st5Data.reduce((acc, curr) => {
    const level = curr.level || 'ไม่ระบุ';
    acc[level] = (acc[level] || 0) + 1;
    return acc;
  }, {});
  const st5PieData = Object.keys(st5Levels).map(key => ({ name: key, value: st5Levels[key] }));
  const ST5_COLORS = ['#34d399', '#fbbf24', '#f43f5e', '#818cf8', '#94a3b8']; 

  const barData = tableData.slice(0, 5);

  // AI Policy Recommendations
  const generateRecommendations = () => {
      let recs = [];
      if (parseFloat(riskPercentage) > 15) {
          recs.push({ title: "🚨 การแทรกแซงเร่งด่วน (Urgent Intervention)", text: "พบสัดส่วนเยาวชนกลุ่มเสี่ยงสูงมากกว่า 15% ควรเร่งประสานผู้เชี่ยวชาญเพื่อจัดกิจกรรมกลุ่มบำบัดด่วนในพื้นที่ที่มีกลุ่มเสี่ยงหนาแน่น" });
      } else {
          recs.push({ title: "🛡️ การรักษาระดับ (Maintenance)", text: "สัดส่วนความเครียดอยู่ในเกณฑ์ที่ควบคุมได้ ควรจัดกิจกรรมส่งเสริมสุขภาพจิตเชิงบวกอย่างต่อเนื่องเพื่อสร้างภูมิคุ้มกันทางใจให้เยาวชน" });
      }
      recs.push({ title: "📊 การติดตามผล (Monitoring)", text: "เน้นย้ำให้พี่เลี้ยงโครงการประเมิน ST-5 ซ้ำในกลุ่มเสี่ยงทุกๆ 2 สัปดาห์ เพื่อติดตามแนวโน้มและการตอบสนองต่อการช่วยเหลืออย่างใกล้ชิด" });
      return recs;
  };
  const recommendations = generateRecommendations();

  // Export PDF Logic
  const handleExportPDF = async () => {
    if (!printRef.current) return;
    setIsExporting(true);
    try {
      const element = printRef.current;
      
      const canvas = await toPng(element, { 
          quality: 1.0, 
          backgroundColor: '#ffffff', 
          pixelRatio: 2
      });
      
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (element.offsetHeight * pdfWidth) / element.offsetWidth; 
      
      pdf.addImage(canvas, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`Executive_Report_${new Date().getTime()}.pdf`);
    } catch (err) {
      console.error(err);
      alert('เกิดข้อผิดพลาดในการสร้าง PDF');
    } finally {
      setIsExporting(false);
    }
  };

  const renderKPIs = () => (
      <>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-blue-50 p-4 rounded-2xl border border-blue-100 text-center shadow-sm">
            <div className="text-blue-500 mb-1 flex justify-center"><Users size={28} /></div>
            <div className="text-3xl font-black text-blue-700">{totalStudents}</div>
            <div className="text-xs font-bold text-blue-600 mt-1">เยาวชนเป้าหมาย (คน)</div>
          </div>
          <div className="bg-emerald-50 p-4 rounded-2xl border border-emerald-100 text-center shadow-sm">
            <div className="text-emerald-500 mb-1 flex justify-center"><BarChart3 size={28} /></div>
            <div className="text-3xl font-black text-emerald-700">{totalEvaluations}</div>
            <div className="text-xs font-bold text-emerald-600 mt-1">การประเมินรวม (ครั้ง)</div>
          </div>
          <div className="bg-rose-50 p-4 rounded-2xl border border-rose-100 text-center shadow-sm">
            <div className="text-rose-500 mb-1 flex justify-center"><AlertCircle size={28} /></div>
            <div className="text-3xl font-black text-rose-700">{st5Risk.length}</div>
            <div className="text-xs font-bold text-rose-600 mt-1">พบกลุ่มเสี่ยง (คน)</div>
          </div>
          <div className="bg-purple-50 p-4 rounded-2xl border border-purple-100 text-center shadow-sm">
            <div className="text-purple-500 mb-1 flex justify-center"><TrendingUp size={28} /></div>
            <div className="text-3xl font-black text-purple-700">{riskPercentage}%</div>
            <div className="text-xs font-bold text-purple-600 mt-1">สัดส่วนกลุ่มเสี่ยง</div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
          <div className="space-y-4">
            <h3 className="text-base font-bold text-slate-700 flex items-center gap-2">
              <RechartsPieChart size={18} className="text-indigo-500" /> สัดส่วนระดับความเครียด
            </h3>
            <div className="h-64 bg-slate-50/50 rounded-2xl p-2 border border-slate-100">
              <ResponsiveContainer width="100%" height="100%">
                <RechartsPieChart>
                  <Pie data={st5PieData} cx="50%" cy="50%" innerRadius={45} outerRadius={70} paddingAngle={2} dataKey="value" label={({name, percent}) => `${name} ${(percent * 100).toFixed(0)}%`} labelLine={false} style={{fontSize: '11px', fontWeight: 'bold', fill: '#475569'}} isAnimationActive={false}>
                    {st5PieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={ST5_COLORS[index % ST5_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </RechartsPieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-base font-bold text-slate-700 flex items-center gap-2">
              <BarChart2 size={18} className="text-teal-500" /> 5 องค์กรที่มีเยาวชนสูงสุด
            </h3>
            <div className="h-64 bg-slate-50/50 rounded-2xl p-2 border border-slate-100">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={barData} margin={{ top: 10, right: 10, left: -20, bottom: 25 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis dataKey="name" tick={{fontSize: 10, fill: '#64748b'}} angle={-45} textAnchor="end" interval={0} />
                  <YAxis tick={{fontSize: 11, fill: '#64748b'}} />
                  <Tooltip cursor={{fill: '#f8fafc'}} />
                  <Bar dataKey="students" name="เยาวชน (คน)" fill="#3b82f6" radius={[4, 4, 0, 0]} isAnimationActive={false} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </>
  );

  const renderTable = () => (
        <div className="space-y-4">
          <h3 className="text-base font-bold text-slate-700 flex items-center gap-2">
            <Layers size={18} className="text-blue-500" /> ข้อมูลแยกตามสังกัด
          </h3>
          <div className="overflow-x-auto rounded-xl border border-slate-200 shadow-sm">
            <table className="w-full text-sm text-left">
              <thead className="bg-slate-50 text-slate-600 font-bold border-b border-slate-200">
                <tr>
                  <th className="px-4 py-3">หน่วยงาน/สถานศึกษา</th>
                  <th className="px-4 py-3 text-center">เยาวชน</th>
                  <th className="px-4 py-3 text-center">ประเมิน ST-5</th>
                  <th className="px-4 py-3 text-center text-rose-600">พบกลุ่มเสี่ยง</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 bg-white">
                {tableData.map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/50 transition-colors">
                    <td className="px-4 py-3 font-medium text-slate-800">{row.name}</td>
                    <td className="px-4 py-3 text-center font-medium">{row.students}</td>
                    <td className="px-4 py-3 text-center text-slate-500">{row.evaluations}</td>
                    <td className="px-4 py-3 text-center font-bold text-rose-600">{row.risk}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
  );

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header & Export Button */}
      <div className="flex flex-col md:flex-row justify-between items-center bg-white p-5 md:p-6 rounded-2xl shadow-sm border border-slate-100 gap-4">
        <div className="text-center md:text-left">
          <h2 className="text-2xl font-black text-slate-800">รายงานสำหรับผู้บริหาร</h2>
          <p className="text-slate-500 text-sm mt-1">ข้อมูลเชิงลึกและบทสรุป (Executive Summary)</p>
        </div>
        <button onClick={handleExportPDF} disabled={isExporting} className="w-full md:w-auto bg-slate-800 hover:bg-slate-700 text-white px-6 py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 shadow-md transition-all">
          {isExporting ? <RefreshCw className="animate-spin" size={18} /> : <FileText size={18} />}
          {isExporting ? 'กำลังประมวลผล PDF...' : 'ส่งออก PDF ฉบับสมบูรณ์'}
        </button>
      </div>

      {/* Interactive Tabs Menu */}
      <div className="flex overflow-x-auto bg-slate-50 p-1.5 rounded-3xl border border-slate-100 shadow-inner hide-on-print snap-x">
        <button onClick={() => setReportTab('kpi')} className={`flex-1 py-3 px-4 rounded-2xl flex items-center justify-center gap-2 text-sm font-bold transition-all whitespace-nowrap snap-center ${reportTab === 'kpi' ? 'bg-white text-pink-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}>
            <LayoutDashboard size={18} /> สรุปภาพรวม (KPIs)
        </button>
        <button onClick={() => setReportTab('mental')} className={`flex-1 py-3 px-4 rounded-2xl flex items-center justify-center gap-2 text-sm font-bold transition-all whitespace-nowrap snap-center ${reportTab === 'mental' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}>
            <Activity size={18} /> สุขภาพจิต (Mental)
        </button>
        <button onClick={() => setReportTab('behavior')} className={`flex-1 py-3 px-4 rounded-2xl flex items-center justify-center gap-2 text-sm font-bold transition-all whitespace-nowrap snap-center ${reportTab === 'behavior' ? 'bg-white text-emerald-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}>
            <Users size={18} /> พฤติกรรม (Behavior)
        </button>
        <button onClick={() => setReportTab('policy')} className={`flex-1 py-3 px-4 rounded-2xl flex items-center justify-center gap-2 text-sm font-bold transition-all whitespace-nowrap snap-center ${reportTab === 'policy' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}>
            <Bot size={18} /> บทวิเคราะห์ AI & นโยบาย
        </button>
      </div>

      {/* Interactive Content Area */}
      <div className="bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-slate-100">
         {reportTab === 'kpi' && (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
               {renderKPIs()}
            </div>
         )}
         
         {reportTab === 'mental' && (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
               {renderTable()}
            </div>
         )}

         {reportTab === 'behavior' && (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500 text-center py-10">
               <ShieldCheck size={48} className="mx-auto text-emerald-300 mb-4" />
               <h3 className="text-xl font-bold text-slate-700">รายงานข้อมูลพฤติกรรม</h3>
               <p className="text-slate-500">รวบรวมข้อมูลพฤติกรรมเชิงบวก และ พฤติกรรมที่ต้องเฝ้าระวังเพื่อใช้ในการวิเคราะห์ต่อไป</p>
            </div>
         )}

         {reportTab === 'policy' && (
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
         )}
      </div>

      {/* ---------------------------------------------------------
          HIDDEN PRINTABLE VIEW (A4 Optimized layout for PDF) 
          --------------------------------------------------------- */}
      <div className="fixed top-[-9999px] left-[-9999px] w-[794px] overflow-hidden pointer-events-none z-[-100]">
        <div ref={printRef} className="w-[794px] bg-white p-12 text-slate-800 space-y-10 print-container" style={{ fontFamily: 'Kanit, sans-serif' }}>
           
           {/* Document Header */}
           <div className="text-center space-y-3 border-b-2 border-slate-800 pb-6">
              <h1 className="text-3xl font-black text-slate-900 tracking-wide">รายงานสรุปผลสัมฤทธิ์ทางการประเมินผู้บริหาร</h1>
              <p className="text-xl font-bold text-slate-600">โครงการพัฒนาทักษะชีวิตและสุขภาพจิตเยาวชน</p>
              <p className="text-sm text-slate-500 font-medium">ข้อมูลประมวลผล ณ วันที่ {new Date().toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
           </div>

           {/* Section 1: KPI */}
           <div className="space-y-4">
             <h2 className="text-xl font-black text-pink-700 flex items-center gap-2 border-l-4 border-pink-500 pl-3">สรุปภาพรวม (KPIs)</h2>
             {renderKPIs()}
           </div>

           <div className="my-8 border-t border-slate-200"></div>

           {/* Section 2: Table Data */}
           <div className="space-y-4">
             <h2 className="text-xl font-black text-blue-700 flex items-center gap-2 border-l-4 border-blue-500 pl-3">สถิติแยกตามหน่วยงาน (สุขภาพจิต)</h2>
             {renderTable()}
           </div>

           <div className="my-8 border-t border-slate-200"></div>

           {/* Section 3: AI Policy */}
           <div className="space-y-6 pb-10">
             <h2 className="text-xl font-black text-indigo-700 flex items-center gap-2 border-l-4 border-indigo-500 pl-3">วิเคราะห์แนวโน้ม และข้อเสนอแนะสำหรับผู้บริหาร</h2>
             <div className="grid grid-cols-1 gap-4">
                 {recommendations.map((rec, idx) => (
                    <div key={idx} className="bg-slate-50 p-5 rounded-xl border border-slate-200">
                       <h4 className="font-bold text-slate-800 text-base mb-1">{rec.title}</h4>
                       <p className="text-slate-600 text-sm leading-relaxed">{rec.text}</p>
                    </div>
                 ))}
             </div>
           </div>
           
           {/* Footer Page */}
           <div className="text-center text-xs text-slate-400 mt-10 pt-4 border-t border-slate-100">
              เอกสารฉบับนี้จัดทำโดยระบบอัตโนมัติ สำหรับใช้เป็นข้อมูลประกอบการตัดสินใจระดับบริหาร
           </div>

        </div>
      </div>

    </div>
  );
}
"""
lines.append(new_component)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.writelines(lines)
