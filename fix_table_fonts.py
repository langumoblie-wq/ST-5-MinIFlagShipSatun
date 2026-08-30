import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_table = """          <div className={`${isPrint ? '' : 'overflow-x-auto'} rounded-xl border border-slate-200 shadow-sm`}>
            <table className="w-full text-sm text-left">
              <thead className="bg-slate-50 text-slate-600 font-bold border-b border-slate-200">
                <tr>
                  <th className="px-4 py-3">หน่วยงาน/สถานศึกษา</th>
                  <th className="px-4 py-3 text-center">เยาวชน</th>
                  <th className="px-4 py-3 text-center">ประเมิน ST-5</th>
                  <th className="px-4 py-3 text-center text-rose-600">พบกลุ่มเสี่ยง</th>
                  <th className="px-4 py-3 text-center text-teal-600">ประเมินพฤติกรรมบวก</th>
                  <th className="px-4 py-3 text-center text-orange-600">ประเมินพฤติกรรมลบ</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 bg-white">
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
              </tbody>
            </table>
          </div>
          <div className="mt-4 p-4 bg-orange-50/50 rounded-2xl border border-orange-100">
            <p className="text-sm font-medium text-orange-800">{tableInterpretation}</p>
          </div>"""

new_table = """          <div className={`${isPrint ? '' : 'overflow-x-auto'} rounded-xl border border-slate-200 shadow-sm`}>
            <table className={`w-full ${isPrint ? 'text-xs' : 'text-sm'} text-left`}>
              <thead className="bg-slate-50 text-slate-600 font-bold border-b border-slate-200">
                <tr>
                  <th className={`px-4 ${isPrint ? 'py-1.5' : 'py-3'}`}>หน่วยงาน/สถานศึกษา</th>
                  <th className={`px-4 ${isPrint ? 'py-1.5' : 'py-3'} text-center`}>เยาวชน</th>
                  <th className={`px-4 ${isPrint ? 'py-1.5' : 'py-3'} text-center`}>ประเมิน ST-5</th>
                  <th className={`px-4 ${isPrint ? 'py-1.5' : 'py-3'} text-center text-rose-600`}>พบกลุ่มเสี่ยง</th>
                  <th className={`px-4 ${isPrint ? 'py-1.5' : 'py-3'} text-center text-teal-600`}>ประเมินพฤติกรรมบวก</th>
                  <th className={`px-4 ${isPrint ? 'py-1.5' : 'py-3'} text-center text-orange-600`}>ประเมินพฤติกรรมลบ</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 bg-white">
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
              </tbody>
            </table>
          </div>
          <div className={`mt-4 p-4 bg-orange-50/50 rounded-2xl border border-orange-100 ${isPrint ? '!p-2 !mt-2' : ''}`}>
            <p className={`${isPrint ? 'text-xs' : 'text-sm'} font-medium text-orange-800`}>{tableInterpretation}</p>
          </div>"""

if old_table in content:
    content = content.replace(old_table, new_table)
    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced Table!")
else:
    print("Table Not found")
