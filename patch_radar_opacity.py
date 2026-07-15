import re

with open('src/App.tsx', 'r') as f:
    code = f.read()

old_radar = """<Radar name="ความถี่พฤติกรรมเชิงบวก" dataKey="A" stroke="#14b8a6" fill="#14b8a6" fillOpacity={0.4} />"""
new_radar = """<Radar name="ความถี่พฤติกรรมเชิงบวก" dataKey="A" stroke="#14b8a6" fill="#14b8a6" fillOpacity={radarMaxPos === 0 ? 0 : 0.4} strokeOpacity={radarMaxPos === 0 ? 0 : 1} />"""

if old_radar in code:
    code = code.replace(old_radar, new_radar)
    with open('src/App.tsx', 'w') as f:
        f.write(code)
    print("Patched radar opacity")
else:
    print("Could not find old radar tag")
