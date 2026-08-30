import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_color_logic = """  const getLevelColor = (level) => {
    if (level === 'เครียดน้อย' || level === 'ปกติ') return '#10b981'; // emerald-500
    if (level === 'เครียดปานกลาง') return '#facc15'; // yellow-400
    if (level === 'เครียดสูง') return '#f97316'; // orange-500
    if (level === 'เครียดรุนแรง') return '#ef4444'; // red-500
    return '#94a3b8'; // slate-400
  };"""

new_color_logic = """  const getLevelColor = (level) => {
    if (level === 'เครียดน้อย' || level === 'ปกติ' || level === 'Low') return '#10b981'; // emerald-500
    if (level === 'เครียดปานกลาง' || level === 'Medium') return '#facc15'; // yellow-400
    if (level === 'เครียดสูง' || level === 'เครียดมาก' || level === 'High') return '#f97316'; // orange-500
    if (level === 'เครียดรุนแรง' || level === 'เครียดมากที่สุด' || level === 'Severe') return '#ef4444'; // red-500
    return '#94a3b8'; // slate-400
  };"""

content = content.replace(old_color_logic, new_color_logic)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
