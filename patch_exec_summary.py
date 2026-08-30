import sys
import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Data Processing
old_data_processing = """  // --- Data Processing ---
  const students = users.filter(u => ['student', 'community'].includes(u.accountType));
  const totalStudents = students.length;
  
  // Link evaluations to students
  const st5Linked = st5Data.filter(d => students.some(s => s.id === d.uid || s.id === d.userId || s.uid === d.uid || s.uid === d.userId));
  const totalEvaluations = st5Linked.length + behaviorData.length; // Or just st5Data if we want all
  
  const st5Risk = st5Linked.filter(d => ['เครียดสูง', 'เครียดรุนแรง'].includes(d.level) || parseInt(d.score) >= 8);
  const riskPercentage = totalStudents > 0 ? ((st5Risk.length / totalStudents) * 100).toFixed(1) : 0;

  const affiliations = [...new Set(students.map(u => u.affiliation).filter(Boolean))];

  // Table Data & Sorting
  const tableData = affiliations.map(aff => {
    const affStudents = students.filter(s => s.affiliation === aff);
    const affSt5 = st5Linked.filter(d => affStudents.some(s => s.id === d.uid || s.id === d.userId || s.uid === d.uid || s.uid === d.userId));
    const affRisk = affSt5.filter(d => ['เครียดสูง', 'เครียดรุนแรง'].includes(d.level) || parseInt(d.score) >= 8).length;
    return { name: aff, students: affStudents.length, evaluations: affSt5.length, risk: affRisk };
  }).sort((a, b) => b.students - a.students);

  // ST-5 Chart Data
  const st5Levels = st5Linked.reduce((acc, curr) => {
    const level = curr.level || 'ไม่ระบุ';
    acc[level] = (acc[level] || 0) + 1;
    return acc;
  }, {});
  const st5PieData = Object.keys(st5Levels).map(key => ({ name: key, value: st5Levels[key] }));
  const ST5_COLORS = ['#34d399', '#fbbf24', '#f43f5e', '#818cf8', '#94a3b8']; 

  const barData = tableData.slice(0, 5);"""

new_data_processing = """  // --- Data Processing ---
  const students = users.filter(u => ['student', 'community'].includes(u.accountType) || u.role === 'user');
  const studentIds = new Set(students.map(u => u.id));
  
  // Link evaluations to students
  const st5Linked = st5Data.filter(d => studentIds.has(d.uid) || studentIds.has(d.userId));
  const behaviorLinked = behaviorData.filter(d => studentIds.has(d.targetUid));
  
  // ยอดคัดกรอง (Unique Screened Users)
  const uniqueScreenedUsers = new Set([
    ...st5Linked.map(d => d.uid || d.userId),
    ...behaviorLinked.map(d => d.targetUid)
  ]);
  const totalScreenedStudents = uniqueScreenedUsers.size;

  const totalEvaluations = st5Linked.length + behaviorLinked.length;
  
  const st5Risk = st5Linked.filter(d => ['เครียดสูง', 'เครียดรุนแรง'].includes(d.level) || parseInt(d.score) >= 8);
  const uniqueRiskUsers = new Set(st5Risk.map(d => d.uid || d.userId));
  
  const riskPercentage = totalScreenedStudents > 0 ? ((uniqueRiskUsers.size / totalScreenedStudents) * 100).toFixed(1) : 0;

  const affiliations = [...new Set(students.map(u => u.affiliation).filter(Boolean))];

  // Table Data & Sorting
  const tableData = affiliations.map(aff => {
    const affStudents = students.filter(s => s.affiliation === aff);
    const affStudentIds = new Set(affStudents.map(s => s.id));
    
    const affSt5 = st5Linked.filter(d => affStudentIds.has(d.uid) || affStudentIds.has(d.userId));
    const affBehaviors = behaviorLinked.filter(d => affStudentIds.has(d.targetUid));
    
    // Unique screened in this affiliation
    const affUniqueScreened = new Set([
      ...affSt5.map(d => d.uid || d.userId),
      ...affBehaviors.map(d => d.targetUid)
    ]).size;
    
    const affRisk = affSt5.filter(d => ['เครียดสูง', 'เครียดรุนแรง'].includes(d.level) || parseInt(d.score) >= 8);
    const affUniqueRisk = new Set(affRisk.map(d => d.uid || d.userId)).size;
    
    return { name: aff, students: affUniqueScreened, evaluations: affSt5.length + affBehaviors.length, risk: affUniqueRisk };
  }).sort((a, b) => b.students - a.students);

  // ST-5 Chart Data
  const st5Levels = st5Linked.reduce((acc, curr) => {
    const level = curr.level || 'ไม่ระบุ';
    acc[level] = (acc[level] || 0) + 1;
    return acc;
  }, {});
  
  const getLevelColor = (level) => {
    if (level === 'เครียดน้อย' || level === 'ปกติ') return '#10b981'; // emerald-500
    if (level === 'เครียดปานกลาง') return '#facc15'; // yellow-400
    if (level === 'เครียดสูง') return '#f97316'; // orange-500
    if (level === 'เครียดรุนแรง') return '#ef4444'; // red-500
    return '#94a3b8'; // slate-400
  };
  
  const st5PieData = Object.keys(st5Levels).map(key => ({ 
    name: key, 
    value: st5Levels[key],
    fill: getLevelColor(key)
  }));

  const barData = tableData.slice(0, 5);"""

content = content.replace(old_data_processing, new_data_processing)

# Replace 'เยาวชนเป้าหมาย (คน)' with 'ยอดคัดกรอง (คน)' and totalStudents with totalScreenedStudents
content = content.replace('{totalStudents}</div>\n            <div className="text-xs font-bold text-blue-600 mt-1">เยาวชนเป้าหมาย (คน)</div>', '{totalScreenedStudents}</div>\n            <div className="text-xs font-bold text-blue-600 mt-1">ยอดคัดกรอง (คน)</div>')
content = content.replace('{st5Risk.length}</div>\n            <div className="text-xs font-bold text-rose-600 mt-1">พบกลุ่มเสี่ยง (คน)', '{uniqueRiskUsers.size}</div>\n            <div className="text-xs font-bold text-rose-600 mt-1">พบกลุ่มเสี่ยง (คน)')

# Replace pie chart Cell rendering
content = re.sub(
    r'<Cell key=\{\`cell-\$\{index\}\`\} fill=\{ST5_COLORS\[index \% ST5_COLORS\.length\]\} />',
    r'<Cell key={`cell-${index}`} fill={entry.fill} />',
    content
)

# Add descriptions under charts
content = re.sub(
    r'(</PieChart>\n\s*</ResponsiveContainer>\n\s*\)\}\n\s*</div>)',
    r'\1\n            <p className="text-xs text-slate-500 text-center px-4">กราฟแสดงสัดส่วนระดับความเครียดของเยาวชนที่ได้รับการประเมิน ST-5 ทั้งหมด โดยแบ่งตามเกณฑ์ของกรมสุขภาพจิต</p>',
    content
)

content = re.sub(
    r'(</BarChart>\n\s*</ResponsiveContainer>\n\s*\)\}\n\s*</div>)',
    r'\1\n            <p className="text-xs text-slate-500 text-center px-4">กราฟแสดง 5 หน่วยงานที่มีจำนวนเยาวชนที่ได้รับการคัดกรองมากที่สุด เพื่อใช้วางแผนการลงพื้นที่</p>',
    content
)

content = re.sub(
    r'(<div className="overflow-x-auto rounded-xl border border-slate-200 shadow-sm">)',
    r'<p className="text-sm text-slate-500 mb-2">ตารางสรุปยอดการคัดกรองพฤติกรรมและความเครียดของเยาวชนในแต่ละสถานศึกษา/ชุมชน พร้อมสัดส่วนกลุ่มเสี่ยงที่ต้องเฝ้าระวัง</p>\n          \1',
    content
)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
