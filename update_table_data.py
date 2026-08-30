import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_table_data = """    const affRisk = affSt5.filter(d => ['เครียดสูง', 'เครียดรุนแรง'].includes(d.level) || parseInt(d.score) >= 8);
    const affUniqueRisk = new Set(affRisk.map(d => d.uid || d.userId)).size;
    
    return { name: aff, students: affUniqueScreened, evaluations: affSt5.length + affBehaviors.length, risk: affUniqueRisk };
  }).sort((a, b) => b.students - a.students);"""

new_table_data = """    const affRisk = affSt5.filter(d => ['เครียดสูง', 'เครียดรุนแรง'].includes(d.level) || parseInt(d.score) >= 8);
    const affUniqueRisk = new Set(affRisk.map(d => d.uid || d.userId)).size;
    
    let goodBehCount = 0;
    let badBehCount = 0;
    affBehaviors.forEach(beh => {
      if (beh.selections && beh.selections.desirable && beh.selections.desirable.length > 0) goodBehCount++;
      if (beh.selections && beh.selections.undesirable && beh.selections.undesirable.length > 0) badBehCount++;
    });
    
    return { 
      name: aff, 
      students: affUniqueScreened, 
      evaluations: affSt5.length + affBehaviors.length, 
      risk: affUniqueRisk,
      goodBeh: goodBehCount,
      badBeh: badBehCount
    };
  }).sort((a, b) => b.students - a.students);"""

content = content.replace(old_table_data, new_table_data)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
