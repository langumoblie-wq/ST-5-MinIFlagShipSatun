import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. We insert the Demographic Logic before generateAIInsights

search_target = """  // --- AI INSIGHTS (Issue Specific) ---"""

demographic_logic = """  // --- DEMOGRAPHIC ANALYSIS ---
  const demographicAnalysis = () => {
    const validUsers = students.filter(u => u.gender || u.age);
    if (validUsers.length === 0) return { hasData: false, insights: ["ยังไม่มีข้อมูลเพศและอายุในระบบ (ผู้ดูแลระบบสามารถเข้าไปแก้ไขข้อมูลผู้ใช้เพื่อเพิ่ม เพศ และ อายุ ได้)"] };
    
    // Process Gender Data
    const byGender = { 'ชาย': { count: 0, st5Sum: 0, st5Count: 0, badBeh: 0, goodBeh: 0 }, 'หญิง': { count: 0, st5Sum: 0, st5Count: 0, badBeh: 0, goodBeh: 0 }, 'อื่นๆ': { count: 0, st5Sum: 0, st5Count: 0, badBeh: 0, goodBeh: 0 } };
    let ageGroups = { 'ต่ำกว่า 15': { count: 0, st5Sum: 0, st5Count: 0, badBeh: 0, goodBeh: 0 }, '15-18': { count: 0, st5Sum: 0, st5Count: 0, badBeh: 0, goodBeh: 0 }, '19 ขึ้นไป': { count: 0, st5Sum: 0, st5Count: 0, badBeh: 0, goodBeh: 0 } };

    validUsers.forEach(u => {
       const uId = u.id;
       const uSt5 = st5Linked.filter(d => d.uid === uId || d.userId === uId);
       const uBeh = behaviorLinked.filter(d => d.targetUid === uId);
       
       let uSt5Score = 0;
       if (uSt5.length > 0) {
           uSt5Score = uSt5.reduce((sum, val) => sum + parseInt(val.score || 0), 0) / uSt5.length;
       }

       let uBad = 0, uGood = 0;
       uBeh.forEach(b => {
           if (b.selections?.undesirable) uBad += b.selections.undesirable.length;
           if (b.selections?.desirable) uGood += b.selections.desirable.length;
       });

       if (u.gender && byGender[u.gender]) {
           byGender[u.gender].count++;
           if (uSt5.length > 0) { byGender[u.gender].st5Sum += uSt5Score; byGender[u.gender].st5Count++; }
           byGender[u.gender].badBeh += uBad;
           byGender[u.gender].goodBeh += uGood;
       }

       if (u.age) {
           const age = parseInt(u.age);
           let group = '';
           if (age < 15) group = 'ต่ำกว่า 15';
           else if (age <= 18) group = '15-18';
           else group = '19 ขึ้นไป';
           
           ageGroups[group].count++;
           if (uSt5.length > 0) { ageGroups[group].st5Sum += uSt5Score; ageGroups[group].st5Count++; }
           ageGroups[group].badBeh += uBad;
           ageGroups[group].goodBeh += uGood;
       }
    });

    let insights = [];
    
    // Gender Insights
    if (byGender['ชาย'].count > 0 && byGender['หญิง'].count > 0) {
        const maleAvgSt5 = byGender['ชาย'].st5Count ? (byGender['ชาย'].st5Sum / byGender['ชาย'].st5Count).toFixed(1) : 0;
        const femaleAvgSt5 = byGender['หญิง'].st5Count ? (byGender['หญิง'].st5Sum / byGender['หญิง'].st5Count).toFixed(1) : 0;
        insights.push(`เพศสัมพันธ์กับความเครียด: เพศหญิงมีคะแนนความเครียดเฉลี่ย (${femaleAvgSt5}) เทียบกับเพศชาย (${maleAvgSt5})`);

        const maleAvgBad = byGender['ชาย'].count ? (byGender['ชาย'].badBeh / byGender['ชาย'].count).toFixed(1) : 0;
        const femaleAvgBad = byGender['หญิง'].count ? (byGender['หญิง'].badBeh / byGender['หญิง'].count).toFixed(1) : 0;
        insights.push(`เพศสัมพันธ์กับพฤติกรรมเสี่ยง: เพศชายพบพฤติกรรมเสี่ยงเฉลี่ย (${maleAvgBad} พฤติกรรม/คน) เทียบกับเพศหญิง (${femaleAvgBad} พฤติกรรม/คน)`);
    }

    // Age Insights
    let maxStressAge = '';
    let maxStressVal = 0;
    Object.keys(ageGroups).forEach(k => {
        if (ageGroups[k].st5Count > 0) {
           const avg = ageGroups[k].st5Sum / ageGroups[k].st5Count;
           if (avg > maxStressVal) { maxStressVal = avg; maxStressAge = k; }
        }
    });
    if (maxStressAge && maxStressVal > 0) {
        insights.push(`อายุสัมพันธ์กับความเครียด: ช่วงอายุ "${maxStressAge}" มีแนวโน้มความเครียดเฉลี่ยสูงสุด (${maxStressVal.toFixed(1)} คะแนน)`);
    }

    return { hasData: true, insights, summary: { gender: byGender, age: ageGroups } };
  };
  const demoData = demographicAnalysis();

  // --- AI INSIGHTS (Issue Specific) ---"""

if search_target in content:
    content = content.replace(search_target, demographic_logic)
    print("Injected demographic analysis logic")
else:
    print("Could not find search_target")

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
