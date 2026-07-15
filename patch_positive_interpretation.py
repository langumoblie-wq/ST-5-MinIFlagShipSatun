import re

with open('src/App.tsx', 'r') as f:
    code = f.read()

old_pos_int = """  const positiveInterpretation = `การแปรผล: จุดแข็งที่พบมากที่สุดคือ "${maxPositive?.subject || 'ไม่มีข้อมูล'}" ควรส่งเสริมเพื่อเป็นปัจจัยปกป้อง`;"""
new_pos_int = """  const positiveInterpretation = radarMaxPos === 0 
    ? 'การแปรผล: ปัจจุบันยังไม่พบข้อมูลพฤติกรรมเชิงบวก' 
    : `การแปรผล: จุดแข็งที่พบมากที่สุดคือ "${maxPositive?.subject || 'ไม่มีข้อมูล'}" ควรส่งเสริมเพื่อเป็นปัจจัยปกป้อง`;"""

if old_pos_int in code:
    code = code.replace(old_pos_int, new_pos_int)
    with open('src/App.tsx', 'w') as f:
        f.write(code)
    print("Patched positive interpretation")
else:
    print("Could not find old pos interpretation")
