import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update ExecutiveAnalyticsDashboard students definition
old_exec_students = "const baseStudents = users.filter(u => ['student', 'community', 'teacher'].includes(u.accountType) && (profile.role === 'superadmin' || u.affiliation === profile.affiliation));"
new_exec_students = "const baseStudents = users.filter(u => (['student', 'community'].includes(u.accountType) || u.role === 'user') && (profile.role === 'superadmin' || u.affiliation === profile.affiliation));"
content = content.replace(old_exec_students, new_exec_students)

# 2. Update chart colors and descriptions in ExecutiveAnalyticsDashboard
old_chart_data = """  const chartDataRisk = [
    { name: 'เครียดน้อย', count: aggregatedData.filter(d => d.riskGroup === 'Low').length, fill: '#5eead4' },
    { name: 'เครียดปานกลาง', count: aggregatedData.filter(d => d.riskGroup === 'Medium').length, fill: '#fcd34d' },
    { name: 'เครียดมาก', count: aggregatedData.filter(d => d.riskGroup === 'High').length, fill: '#fca5a5' },
    { name: 'เครียดมากที่สุด', count: aggregatedData.filter(d => d.riskGroup === 'Severe').length, fill: '#f87171' },
  ];"""

new_chart_data = """  const chartDataRisk = [
    { name: 'เครียดน้อย (ปกติ)', count: aggregatedData.filter(d => d.riskGroup === 'Low').length, fill: '#10b981' }, // emerald-500
    { name: 'เครียดปานกลาง', count: aggregatedData.filter(d => d.riskGroup === 'Medium').length, fill: '#facc15' }, // yellow-400
    { name: 'เครียดสูง', count: aggregatedData.filter(d => d.riskGroup === 'High').length, fill: '#f97316' }, // orange-500
    { name: 'เครียดรุนแรง', count: aggregatedData.filter(d => d.riskGroup === 'Severe').length, fill: '#ef4444' }, // red-500
  ];"""
content = content.replace(old_chart_data, new_chart_data)

# Add descriptions in ExecutiveAnalyticsDashboard
content = re.sub(
    r'(<BarChart data=\{chartDataRisk\}.*?</ResponsiveContainer>\n\s*</div>)',
    r'\1\n                <p className="text-xs text-slate-500 text-center mt-2 px-2">แผนภูมิแสดงสัดส่วนของเยาวชนในแต่ละระดับความเครียด เพื่อใช้ประเมินสถานการณ์สุขภาพจิตโดยรวม</p>',
    content,
    flags=re.DOTALL
)

content = re.sub(
    r'(<AreaChart data=\{.*?\}</ResponsiveContainer>\n\s*</div>)',
    r'\1\n                <p className="text-xs text-slate-500 text-center mt-2 px-2">กราฟเส้นแสดงแนวโน้มการเปลี่ยนแปลงของคะแนนความเครียดเฉลี่ยในแต่ละช่วงเวลา</p>',
    content,
    flags=re.DOTALL
)

content = re.sub(
    r'(<BarChart data=\{radarData\}.*?</ResponsiveContainer>\n\s*</div>)',
    r'\1\n                <p className="text-xs text-slate-500 text-center mt-2 px-2">แผนภูมิแท่งแสดงความถี่ของพฤติกรรมแต่ละประเภทที่ตรวจพบในกลุ่มเยาวชน</p>',
    content,
    flags=re.DOTALL
)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
