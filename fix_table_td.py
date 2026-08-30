import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_tbody = """              <tbody className="divide-y divide-slate-100 bg-white">
                {tableData.map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/50 transition-colors">
                    <td className="px-4 py-3 font-medium text-slate-800">{row.name}</td>
                    <td className="px-4 py-3 text-center font-medium">{row.students}</td>
                    <td className="px-4 py-3 text-center text-slate-500">{row.evaluations}</td>
                    <td className="px-4 py-3 text-center font-bold text-rose-600">{row.risk}</td>
                  </tr>
                ))}
              </tbody>"""

new_tbody = """              <tbody className="divide-y divide-slate-100 bg-white">
                {tableData.map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/50 transition-colors">
                    <td className={`px-4 ${isPrint ? 'py-1.5' : 'py-3'} font-medium text-slate-800`}>{row.name}</td>
                    <td className={`px-4 ${isPrint ? 'py-1.5' : 'py-3'} text-center font-medium`}>{row.students}</td>
                    <td className={`px-4 ${isPrint ? 'py-1.5' : 'py-3'} text-center text-slate-500`}>{row.evaluations}</td>
                    <td className={`px-4 ${isPrint ? 'py-1.5' : 'py-3'} text-center font-bold text-rose-600`}>{row.risk}</td>
                    <td className={`px-4 ${isPrint ? 'py-1.5' : 'py-3'} text-center font-bold text-teal-600`}>{row.goodBeh}</td>
                    <td className={`px-4 ${isPrint ? 'py-1.5' : 'py-3'} text-center font-bold text-orange-600`}>{row.badBeh}</td>
                  </tr>
                ))}
              </tbody>"""

if old_tbody in content:
    content = content.replace(old_tbody, new_tbody)
    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced!")
else:
    print("Not found")
