import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_code = """  // ST-5 Chart Data
  const st5Levels = st5Linked.reduce((acc, curr) => {
    const level = curr.level || 'ไม่ระบุ';
    acc[level] = (acc[level] || 0) + 1;
    return acc;
  }, {});
  
  const getLevelColor = (level) => {
    if (level === 'เครียดน้อย' || level === 'ปกติ' || level === 'Low') return '#10b981'; // emerald-500
    if (level === 'เครียดปานกลาง' || level === 'Medium') return '#facc15'; // yellow-400
    if (level === 'เครียดสูง' || level === 'เครียดมาก' || level === 'High') return '#f97316'; // orange-500
    if (level === 'เครียดรุนแรง' || level === 'เครียดมากที่สุด' || level === 'Severe') return '#ef4444'; // red-500
    return '#94a3b8'; // slate-400
  };
  
  const st5PieData = Object.keys(st5Levels).map(key => ({ 
    name: key, 
    value: st5Levels[key],
    fill: getLevelColor(key)
  }));
  
  const maxSt5Level = st5PieData.reduce((max, current) => current.value > (max?.value || 0) ? current : max, st5PieData[0]);
  const st5PieInterpretation = st5Linked.length === 0 
    ? 'การแปรผล: ยังไม่มีข้อมูลการประเมิน ST-5'
    : `การแปรผล: เยาวชนส่วนใหญ่อยู่ในกลุ่ม "${maxSt5Level?.name || 'ไม่มีข้อมูล'}" คิดเป็น ${Math.round((maxSt5Level?.value / st5Linked.length) * 100)}% ของผู้รับการประเมินทั้งหมด`;"""

new_code = """  // ST-5 Chart Data (Aligned with Executive Dashboard - latest evaluation per user)
  let riskCounts = {
    'Low': 0,
    'Medium': 0,
    'High': 0,
    'Severe': 0
  };
  let validSt5Count = 0;

  students.forEach(user => {
    const uSt5 = st5Linked.filter(s => s.uid === user.id || s.userId === user.id);
    if (uSt5.length > 0) {
      const latestScore = uSt5[0].score;
      const risk = calculateST5(latestScore).risk;
      if (riskCounts[risk] !== undefined) {
        riskCounts[risk]++;
        validSt5Count++;
      }
    }
  });

  const st5PieData = [
    { name: 'เครียดน้อย (ปกติ)', value: riskCounts['Low'], fill: '#10b981' },
    { name: 'เครียดปานกลาง', value: riskCounts['Medium'], fill: '#facc15' },
    { name: 'เครียดสูง', value: riskCounts['High'], fill: '#f97316' },
    { name: 'เครียดรุนแรง', value: riskCounts['Severe'], fill: '#ef4444' }
  ].filter(d => d.value > 0);
  
  const maxSt5Level = st5PieData.length > 0 ? st5PieData.reduce((max, current) => current.value > (max?.value || 0) ? current : max, st5PieData[0]) : null;
  const st5PieInterpretation = validSt5Count === 0 
    ? 'การแปรผล: ยังไม่มีข้อมูลการประเมิน ST-5'
    : `การแปรผล: เยาวชนส่วนใหญ่อยู่ในกลุ่ม "${maxSt5Level?.name || 'ไม่มีข้อมูล'}" คิดเป็น ${Math.round((maxSt5Level?.value / validSt5Count) * 100)}% ของผู้รับการประเมินทั้งหมด`;"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Pie chart code replaced!")
else:
    print("Pie chart code NOT found!")

