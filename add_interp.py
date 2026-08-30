import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Generate interpretation strings for ExecutiveSummaryReport
old_st5_pie_def = """  const st5PieData = Object.keys(st5Levels).map(key => ({ 
    name: key, 
    value: st5Levels[key],
    fill: getLevelColor(key)
  }));

  const barData = tableData.slice(0, 5);"""

new_st5_pie_def = """  const st5PieData = Object.keys(st5Levels).map(key => ({ 
    name: key, 
    value: st5Levels[key],
    fill: getLevelColor(key)
  }));
  
  const maxSt5Level = st5PieData.reduce((max, current) => current.value > (max?.value || 0) ? current : max, st5PieData[0]);
  const st5PieInterpretation = st5Linked.length === 0 
    ? 'การแปรผล: ยังไม่มีข้อมูลการประเมิน ST-5'
    : `การแปรผล: เยาวชนส่วนใหญ่อยู่ในกลุ่ม "${maxSt5Level?.name || 'ไม่มีข้อมูล'}" คิดเป็น ${Math.round((maxSt5Level?.value / st5Linked.length) * 100)}% ของผู้รับการประเมินทั้งหมด`;

  const barData = tableData.slice(0, 5);
  const maxAffiliation = barData[0];
  const barInterpretation = maxAffiliation 
    ? `การแปรผล: องค์กร/สถานที่ที่มีเยาวชนเข้ารับการประเมินสูงสุดคือ "${maxAffiliation.name}" (จำนวน ${maxAffiliation.students} คน) ควรจัดสรรทรัพยากรพี่เลี้ยงให้เหมาะสมกับสัดส่วนนี้`
    : 'การแปรผล: ยังไม่มีข้อมูลจำนวนเยาวชนในระบบ';
"""

content = content.replace(old_st5_pie_def, new_st5_pie_def)

# Add it under the PieChart
old_pie_desc = '<p className="text-xs text-slate-500 text-center px-4">กราฟแสดงสัดส่วนระดับความเครียดของเยาวชนที่ได้รับการประเมิน ST-5 ทั้งหมด โดยแบ่งตามเกณฑ์ของกรมสุขภาพจิต</p>'
new_pie_desc = """<p className="text-xs text-slate-500 text-center px-4">กราฟแสดงสัดส่วนระดับความเครียดของเยาวชนที่ได้รับการประเมิน ST-5 ทั้งหมด โดยแบ่งตามเกณฑ์ของกรมสุขภาพจิต</p>
            <div className="mt-4 p-4 bg-indigo-50/50 rounded-2xl border border-indigo-100">
              <p className="text-sm font-medium text-indigo-800">{st5PieInterpretation}</p>
            </div>"""
content = content.replace(old_pie_desc, new_pie_desc)

# Add it under the BarChart
old_bar_desc = '<p className="text-xs text-slate-500 text-center px-4">กราฟแสดง 5 หน่วยงานที่มีจำนวนเยาวชนที่ได้รับการคัดกรองมากที่สุด เพื่อใช้วางแผนการลงพื้นที่</p>'
new_bar_desc = """<p className="text-xs text-slate-500 text-center px-4">กราฟแสดง 5 หน่วยงานที่มีจำนวนเยาวชนที่ได้รับการคัดกรองมากที่สุด เพื่อใช้วางแผนการลงพื้นที่</p>
            <div className="mt-4 p-4 bg-teal-50/50 rounded-2xl border border-teal-100">
              <p className="text-sm font-medium text-teal-800">{barInterpretation}</p>
            </div>"""
content = content.replace(old_bar_desc, new_bar_desc)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
