import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Behavior processing logic inside ExecutiveSummaryReport

# Find the end of data processing logic
search_target = """  const recommendations = generateRecommendations();"""

insertion = """  const recommendations = generateRecommendations();

  // --- ADD BEHAVIOR LOGIC ---
  const posBehaviorsList = [
    "การใฝ่เรียนรู้", "การคิดวิเคราะห์", "การแก้ปัญหา", 
    "การควบคุมอารมณ์", "ความเห็นอกเห็นใจผู้อื่น", "ความภาคภูมิใจในตนเอง", 
    "ความรับผิดชอบและวินัย", "จิตสาธารณะ", "การดูแลสุขภาพกาย"
  ];
  
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

  let badCategories = {};
  let goodCategories = {};
  behaviorLinked.forEach(beh => {
    if (beh.selections && beh.selections.undesirable) {
      beh.selections.undesirable.forEach(item => { badCategories[item] = (badCategories[item] || 0) + 1; });
    }
    if (beh.selections && beh.selections.desirable) {
      beh.selections.desirable.forEach(item => { goodCategories[item] = (goodCategories[item] || 0) + 1; });
    }
  });

  const radarData = posBehaviorsList.map(item => ({
    subject: item.replace('การ', '').replace('ความ', ''), 
    A: goodCategories[item] || 0,
    fullMark: totalScreenedStudents || 1
  }));
  const radarMaxPos = Math.max(...radarData.map(d => d.A));
  const radarDomainMax = radarMaxPos === 0 ? 1 : 'dataMax';

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
      count: badCategories[item] || 0
    };
  }).sort((a, b) => b.count - a.count);
  
  const maxPositive = radarData.reduce((max, current) => current.A > (max?.A || 0) ? current : max, radarData[0]);
  const positiveInterpretation = radarMaxPos === 0 
    ? 'การแปรผล: ปัจจุบันยังไม่พบข้อมูลพฤติกรรมเชิงบวก' 
    : `การแปรผล: จุดแข็งที่พบมากที่สุดคือ "${maxPositive?.subject || 'ไม่มีข้อมูล'}" ควรส่งเสริมเพื่อเป็นปัจจัยปกป้อง`;

  const maxNegative = negativeChartData[0];
  const negativeInterpretation = maxNegative?.count === 0 
    ? 'การแปรผล: ปัจจุบันยังไม่พบข้อมูลพฤติกรรมเสี่ยง' 
    : `การแปรผล: พฤติกรรมเสี่ยงที่พบมากที่สุดคือ "${maxNegative?.name || 'ไม่มีข้อมูล'}" (${maxNegative?.count} ครั้ง) ควรเฝ้าระวังอย่างใกล้ชิด`;

  // --- AI INSIGHTS (Issue Specific) ---
  const generateAIInsights = () => {
    let insights = [];
    if (totalScreenedStudents < 5) return ["ข้อมูลยังไม่เพียงพอสำหรับการวิเคราะห์เชิงลึกด้วย AI (ต้องการข้อมูลอย่างน้อย 5 เคส)"];
    
    // Insight 1: Physical Health vs Gaming/Stress
    const lowHealthCount = radarData.find(d => d.subject === "ดูแลสุขภาพกาย")?.A || 0;
    const gamingCount = negativeChartData.find(d => d.name === "ติดสื่อออนไลน์")?.count || 0;
    if (lowHealthCount === 0 && gamingCount > 0) {
        insights.push(`พบความเชื่อมโยงน่าสนใจ: มีแนวโน้มที่เยาวชนขาดการดูแลสุขภาพกายจะสัมพันธ์กับพฤติกรรมติดสื่อออนไลน์ (${gamingCount} เคส)`);
    }

    // Insight 2: Self-esteem vs Bullying
    const esteemCount = radarData.find(d => d.subject === "ภาคภูมิใจในตนเอง")?.A || 0;
    const bullyingCount = negativeChartData.find(d => d.name === "Bullying")?.count || 0;
    if (esteemCount === 0 && bullyingCount > 0) {
        insights.push(`พฤติกรรมการรังแกกัน (Bullying) ${bullyingCount} เคส มักเกิดควบคู่กับการขาดความภาคภูมิใจในตนเอง`);
    }

    if (insights.length === 0) {
      insights.push("ระดับสุขภาพจิตและพฤติกรรมของประชากรกลุ่มนี้ยังอยู่ในเกณฑ์ที่ควบคุมได้ดี ไม่มีสัญญาณเตือนภัยเชิงพฤติกรรมร่วมที่น่ากังวลแบบก้าวกระโดด");
    }

    return insights;
  };
  const aiInsightTexts = generateAIInsights();
"""

if search_target in content:
    content = content.replace(search_target, insertion)
    print("Added behavior variables.")
else:
    print("Could not find search_target.")

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
