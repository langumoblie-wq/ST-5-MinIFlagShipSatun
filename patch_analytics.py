import re

with open('src/App.tsx', 'r') as f:
    code = f.read()

# Update negBehaviorsList and mapping
old_neg_logic = """  // --- NEGATIVE BEHAVIORS DATA ---
  const negBehaviorsList = [
    "การใช้ความรุนแรงและรังแกกัน (Bullying)", "การใช้สารเสพติด", "การพนัน", "การหนีเรียน", "การหมกมุ่นกับสื่อออนไลน์"
  ];
  const negativeChartData = negBehaviorsList.map(item => ({
    name: item.replace('การ', '').replace('ความรุนแรงและรังแกกัน (Bullying)', 'Bullying').replace('หมกมุ่นกับสื่อออนไลน์', 'ติดเกม/สื่อ'),
    count: countBehavior(item, 'bad')
  })).sort((a, b) => b.count - a.count);"""

new_neg_logic = """  // --- NEGATIVE BEHAVIORS DATA ---
  const negBehaviorsList = [
    "การใช้ความรุนแรงและรังแกกัน (Bullying)", 
    "การก่อความเดือดร้อนรำคาญ",
    "การใช้สารเสพติด", 
    "การพนัน", 
    "พฤติกรรมทางเพศที่ไม่ปลอดภัย",
    "ภาวะซึมเศร้าและวิตกกังวล",
    "อารมณ์ฉุนเฉียวและก้าวร้าว",
    "การหนีเรียน", 
    "พฤติกรรมถดถอยในการเรียน",
    "การหมกมุ่นกับสื่อออนไลน์"
  ];

  const negativeChartData = negBehaviorsList.map(item => {
    let shortName = item;
    if (item === "การใช้ความรุนแรงและรังแกกัน (Bullying)") shortName = "Bullying";
    else if (item === "การก่อความเดือดร้อนรำคาญ") shortName = "เดือดร้อนรำคาญ";
    else if (item === "การใช้สารเสพติด") shortName = "สารเสพติด";
    else if (item === "การพนัน") shortName = "พนัน";
    else if (item === "พฤติกรรมทางเพศที่ไม่ปลอดภัย") shortName = "พฤติกรรมทางเพศ";
    else if (item === "ภาวะซึมเศร้าและวิตกกังวล") shortName = "ซึมเศร้า/วิตกกังวล";
    else if (item === "อารมณ์ฉุนเฉียวและก้าวร้าว") shortName = "ก้าวร้าว";
    else if (item === "การหนีเรียน") shortName = "หนีเรียน";
    else if (item === "พฤติกรรมถดถอยในการเรียน") shortName = "เรียนถดถอย";
    else if (item === "การหมกมุ่นกับสื่อออนไลน์") shortName = "ติดสื่อออนไลน์";
    
    return {
      name: shortName,
      count: countBehavior(item, 'bad')
    };
  }).sort((a, b) => b.count - a.count);

  const radarMaxPos = Math.max(...radarData.map(d => d.A));
  const radarDomainMax = radarMaxPos === 0 ? 1 : 'dataMax';"""

if old_neg_logic in code:
    code = code.replace(old_neg_logic, new_neg_logic)
    print("Patched negative behavior logic")
else:
    print("Could not find old_neg_logic")

old_radar_chart = """                    <PolarRadiusAxis angle={30} domain={[0, 'dataMax']} tick={false} axisLine={false}/>"""
new_radar_chart = """                    <PolarRadiusAxis angle={30} domain={[0, radarDomainMax]} tick={false} axisLine={false}/>"""

if old_radar_chart in code:
    code = code.replace(old_radar_chart, new_radar_chart)
    print("Patched radar chart")
else:
    print("Could not find old_radar_chart")

with open('src/App.tsx', 'w') as f:
    f.write(code)
