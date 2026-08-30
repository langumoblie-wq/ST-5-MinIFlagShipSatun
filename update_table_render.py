import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_thead = """                <tr>
                  <th className="px-4 py-3">หน่วยงาน/สถานศึกษา</th>
                  <th className="px-4 py-3 text-center">เยาวชน</th>
                  <th className="px-4 py-3 text-center">ประเมิน ST-5</th>
                  <th className="px-4 py-3 text-center text-rose-600">พบกลุ่มเสี่ยง</th>
                </tr>"""

new_thead = """                <tr>
                  <th className="px-4 py-3">หน่วยงาน/สถานศึกษา</th>
                  <th className="px-4 py-3 text-center">เยาวชน</th>
                  <th className="px-4 py-3 text-center">ประเมิน ST-5</th>
                  <th className="px-4 py-3 text-center text-rose-600">พบกลุ่มเสี่ยง</th>
                  <th className="px-4 py-3 text-center text-teal-600">ประเมินพฤติกรรมบวก</th>
                  <th className="px-4 py-3 text-center text-orange-600">ประเมินพฤติกรรมลบ</th>
                </tr>"""

content = content.replace(old_thead, new_thead)

old_tbody = """                {tableData.map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/50 transition-colors">
                    <td className="px-4 py-3 font-medium text-slate-800">{row.name}</td>
                    <td className="px-4 py-3 text-center">{row.students}</td>
                    <td className="px-4 py-3 text-center">{row.evaluations}</td>
                    <td className="px-4 py-3 text-center text-rose-600 font-bold">{row.risk > 0 ? row.risk : '-'}</td>
                  </tr>
                ))}"""

new_tbody = """                {tableData.map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/50 transition-colors">
                    <td className="px-4 py-3 font-medium text-slate-800">{row.name}</td>
                    <td className="px-4 py-3 text-center">{row.students}</td>
                    <td className="px-4 py-3 text-center">{row.evaluations}</td>
                    <td className="px-4 py-3 text-center text-rose-600 font-bold">{row.risk > 0 ? row.risk : '-'}</td>
                    <td className="px-4 py-3 text-center text-teal-600 font-medium">{row.goodBeh > 0 ? row.goodBeh : '-'}</td>
                    <td className="px-4 py-3 text-center text-orange-600 font-medium">{row.badBeh > 0 ? row.badBeh : '-'}</td>
                  </tr>
                ))}"""

content = content.replace(old_tbody, new_tbody)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
