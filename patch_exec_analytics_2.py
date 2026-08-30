import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix totalEvaluated in ExecutiveAnalyticsDashboard
old_eval = """  const validForCorrelation = aggregatedData.filter(d => d.st5Score !== null);
  const totalEvaluated = validForCorrelation.length;"""
new_eval = """  const validForCorrelation = aggregatedData.filter(d => d.st5Score !== null);
  const evaluatedUsers = aggregatedData.filter(d => d.st5Score !== null || d.totalBadBehaviors > 0 || d.totalGoodBehaviors > 0);
  const totalEvaluated = evaluatedUsers.length;"""
content = content.replace(old_eval, new_eval)

# Replace label 'ผู้ตอบแบบประเมิน' -> 'ยอดคัดกรอง (คน)'
old_label = '{totalEvaluated}</p>\n              <p className="text-[10px] font-bold text-slate-400 uppercase mt-1">ผู้ตอบแบบประเมิน</p>'
new_label = '{totalEvaluated}</p>\n              <p className="text-[10px] font-bold text-slate-400 uppercase mt-1">ยอดคัดกรอง (คน)</p>'
content = content.replace(old_label, new_label)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
