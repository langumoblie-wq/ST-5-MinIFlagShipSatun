import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to replace demographicAnalysis logic with the advanced one

search_target = """  // --- DEMOGRAPHIC ANALYSIS ---
  const demographicAnalysis = () => {"""

end_target = """  const demoData = demographicAnalysis();"""

start_idx = content.find(search_target)
end_idx = content.find(end_target) + len(end_target)

if start_idx == -1 or end_idx == -1:
    print("Could not find demographic analysis block")
    exit(1)

new_logic = """  // --- DEMOGRAPHIC ANALYSIS ---
  const demographicAnalysis = () => {
    const validUsers = students.filter(u => u.gender || u.age);
    if (validUsers.length === 0) return { hasData: false, insights: ["ยังไม่มีข้อมูลเพศและอายุในระบบ (ผู้ดูแลระบบสามารถเข้าไปแก้ไขข้อมูลผู้ใช้เพื่อเพิ่ม เพศ และ อายุ ได้)"] };
    
    // Process Gender Data
    const byGender = { 'ชาย': { count: 0, st5Sum: 0, st5Count: 0, badBeh: 0, goodBeh: 0, st5Items: [0,0,0,0,0] }, 'หญิง': { count: 0, st5Sum: 0, st5Count: 0, badBeh: 0, goodBeh: 0, st5Items: [0,0,0,0,0] }, 'อื่นๆ': { count: 0, st5Sum: 0, st5Count: 0, badBeh: 0, goodBeh: 0, st5Items: [0,0,0,0,0] } };
    let ageGroups = { 'ต่ำกว่า 15': { count: 0, st5Sum: 0, st5Count: 0, badBeh: 0, goodBeh: 0, st5Items: [0,0,0,0,0] }, '15-18': { count: 0, st5Sum: 0, st5Count: 0, badBeh: 0, goodBeh: 0, st5Items: [0,0,0,0,0] }, '19 ขึ้นไป': { count: 0, st5Sum: 0, st5Count: 0, badBeh: 0, goodBeh: 0, st5Items: [0,0,0,0,0] } };

    validUsers.forEach(u => {
       const uId = u.id;
       const uSt5 = st5Linked.filter(d => d.uid === uId || d.userId === uId);
       const uBeh = behaviorLinked.filter(d => d.targetUid === uId);
       
       let uSt5Score = 0;
       let uSt5Answers = [0,0,0,0,0];
       if (uSt5.length > 0) {
           uSt5Score = uSt5.reduce((sum, val) => sum + parseInt(val.score || 0), 0) / uSt5.length;
           // Find latest ST-5 for detailed item analysis
           const latest = [...uSt5].sort((a, b) => b.timestamp - a.timestamp)[0];
           if (latest.answers && latest.answers.length === 5) {
               uSt5Answers = latest.answers;
           }
       }

       let uBad = 0, uGood = 0;
       uBeh.forEach(b => {
           if (b.selections?.undesirable) uBad += b.selections.undesirable.length;
           if (b.selections?.desirable) uGood += b.selections.desirable.length;
       });

       if (u.gender && byGender[u.gender]) {
           byGender[u.gender].count++;
           if (uSt5.length > 0) { 
               byGender[u.gender].st5Sum += uSt5Score; 
               byGender[u.gender].st5Count++; 
               for(let i=0;i<5;i++) byGender[u.gender].st5Items[i] += uSt5Answers[i];
           }
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
           if (uSt5.length > 0) { 
               ageGroups[group].st5Sum += uSt5Score; 
               ageGroups[group].st5Count++; 
               for(let i=0;i<5;i++) ageGroups[group].st5Items[i] += uSt5Answers[i];
           }
           ageGroups[group].badBeh += uBad;
           ageGroups[group].goodBeh += uGood;
       }
    });

    let insights = [];
    const st5Questions = [
      "มีปัญหาการนอน", "สมาธิน้อยลง", "หงุดหงิด/ว้าวุ่นใจ", "รู้สึกเบื่อ เซ็ง", "ไม่อยากพบปะผู้คน"
    ];
    
    // Gender Insights
    if (byGender['ชาย'].count > 0 && byGender['หญิง'].count > 0) {
        const maleAvgSt5 = byGender['ชาย'].st5Count ? (byGender['ชาย'].st5Sum / byGender['ชาย'].st5Count).toFixed(1) : 0;
        const femaleAvgSt5 = byGender['หญิง'].st5Count ? (byGender['หญิง'].st5Sum / byGender['หญิง'].st5Count).toFixed(1) : 0;
        insights.push(`เพศสัมพันธ์กับความเครียด: เพศหญิงมีคะแนนความเครียดรวมเฉลี่ย (${femaleAvgSt5}) เทียบกับเพศชาย (${maleAvgSt5})`);

        const maleAvgBad = byGender['ชาย'].count ? (byGender['ชาย'].badBeh / byGender['ชาย'].count).toFixed(1) : 0;
        const femaleAvgBad = byGender['หญิง'].count ? (byGender['หญิง'].badBeh / byGender['หญิง'].count).toFixed(1) : 0;
        insights.push(`เพศสัมพันธ์กับพฤติกรรม: เพศชายพบพฤติกรรมเสี่ยงเฉลี่ย (${maleAvgBad} พฤติกรรม/คน) เทียบกับเพศหญิง (${femaleAvgBad} พฤติกรรม/คน)`);
        
        // Detailed ST-5 by gender
        let highestMaleItem = 0, highestMaleItemScore = 0;
        let highestFemaleItem = 0, highestFemaleItemScore = 0;
        for(let i=0;i<5;i++) {
            const mScore = byGender['ชาย'].st5Count ? byGender['ชาย'].st5Items[i]/byGender['ชาย'].st5Count : 0;
            const fScore = byGender['หญิง'].st5Count ? byGender['หญิง'].st5Items[i]/byGender['หญิง'].st5Count : 0;
            if(mScore > highestMaleItemScore) { highestMaleItemScore = mScore; highestMaleItem = i; }
            if(fScore > highestFemaleItemScore) { highestFemaleItemScore = fScore; highestFemaleItem = i; }
        }
        if (byGender['ชาย'].st5Count > 0) insights.push(`ปัญหาสุขภาพจิตรายข้อ (ชาย): พบปัญหา "${st5Questions[highestMaleItem]}" สูงที่สุด`);
        if (byGender['หญิง'].st5Count > 0) insights.push(`ปัญหาสุขภาพจิตรายข้อ (หญิง): พบปัญหา "${st5Questions[highestFemaleItem]}" สูงที่สุด`);
    }

    // Age Insights
    let maxStressAge = '';
    let maxStressVal = 0;
    let maxStressAgeItem = 0;
    let maxStressAgeItemVal = 0;
    Object.keys(ageGroups).forEach(k => {
        if (ageGroups[k].st5Count > 0) {
           const avg = ageGroups[k].st5Sum / ageGroups[k].st5Count;
           if (avg > maxStressVal) { 
               maxStressVal = avg; 
               maxStressAge = k;
               // Find worst item for this age group
               for(let i=0;i<5;i++) {
                   const itemAvg = ageGroups[k].st5Items[i]/ageGroups[k].st5Count;
                   if (itemAvg > maxStressAgeItemVal) { maxStressAgeItemVal = itemAvg; maxStressAgeItem = i; }
               }
           }
        }
    });
    if (maxStressAge && maxStressVal > 0) {
        insights.push(`อายุสัมพันธ์กับความเครียด: ช่วงอายุ "${maxStressAge}" มีความเครียดสูงสุดเฉลี่ย (${maxStressVal.toFixed(1)} คะแนน) โดยมีปัญหาหลักรายข้อคือ "${st5Questions[maxStressAgeItem]}"`);
    }

    return { hasData: true, insights, summary: { gender: byGender, age: ageGroups } };
  };
  const demoData = demographicAnalysis();"""

content = content[:start_idx] + new_logic + content[end_idx:]

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
