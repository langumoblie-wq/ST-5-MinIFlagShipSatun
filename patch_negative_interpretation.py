import re

with open('src/App.tsx', 'r') as f:
    code = f.read()

old_interpretation = """  const negativeInterpretation = `การแปรผล: พฤติกรรมเสี่ยงที่พบสูงสุดคือ "${maxNegative?.name || 'ไม่มีข้อมูล'}" ควรมีมาตรการดูแลอย่างใกล้ชิด`;"""
new_interpretation = """  const negativeInterpretation = maxNegative?.count === 0 
    ? 'การแปรผล: ปัจจุบันยังไม่พบพฤติกรรมเสี่ยงที่ต้องเฝ้าระวัง' 
    : `การแปรผล: พฤติกรรมเสี่ยงที่พบสูงสุดคือ "${maxNegative?.name || 'ไม่มีข้อมูล'}" ควรมีมาตรการดูแลอย่างใกล้ชิด`;"""

if old_interpretation in code:
    code = code.replace(old_interpretation, new_interpretation)
    with open('src/App.tsx', 'w') as f:
        f.write(code)
    print("Patched negative interpretation")
else:
    print("Could not find old interpretation")
