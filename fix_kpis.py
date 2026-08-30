import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_kpis = """  const renderKPIs = (isPrint = false) => (
      <>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-blue-50 p-4 rounded-2xl border border-blue-100 text-center shadow-sm">
            <div className="text-blue-500 mb-1 flex justify-center"><Users size={28} /></div>
            <div className="text-3xl font-black text-blue-700">{totalScreenedStudents}</div>
            <div className="text-xs font-bold text-blue-600 mt-1">ยอดคัดกรอง (คน)</div>
          </div>
          <div className="bg-emerald-50 p-4 rounded-2xl border border-emerald-100 text-center shadow-sm">
            <div className="text-emerald-500 mb-1 flex justify-center"><BarChart3 size={28} /></div>
            <div className="text-3xl font-black text-emerald-700">{totalEvaluations}</div>
            <div className="text-xs font-bold text-emerald-600 mt-1">การประเมินรวม (ครั้ง)</div>
          </div>
          <div className="bg-rose-50 p-4 rounded-2xl border border-rose-100 text-center shadow-sm">
            <div className="text-rose-500 mb-1 flex justify-center"><AlertCircle size={28} /></div>
            <div className="text-3xl font-black text-rose-700">{uniqueRiskUsers.size}</div>
            <div className="text-xs font-bold text-rose-600 mt-1">พบกลุ่มเสี่ยง (คน)</div>
          </div>
          <div className="bg-purple-50 p-4 rounded-2xl border border-purple-100 text-center shadow-sm">
            <div className="text-purple-500 mb-1 flex justify-center"><TrendingUp size={28} /></div>
            <div className="text-3xl font-black text-purple-700">{riskPercentage}%</div>
            <div className="text-xs font-bold text-purple-600 mt-1">สัดส่วนกลุ่มเสี่ยง</div>
          </div>
        </div>"""

new_kpis = """  const renderKPIs = (isPrint = false) => (
      <>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className={`bg-blue-50 ${isPrint ? 'p-2' : 'p-4'} rounded-2xl border border-blue-100 text-center shadow-sm`}>
            <div className="text-blue-500 mb-1 flex justify-center"><Users size={isPrint ? 20 : 28} /></div>
            <div className={`${isPrint ? 'text-2xl' : 'text-3xl'} font-black text-blue-700`}>{totalScreenedStudents}</div>
            <div className={`${isPrint ? 'text-[10px]' : 'text-xs'} font-bold text-blue-600 mt-1`}>ยอดคัดกรอง (คน)</div>
          </div>
          <div className={`bg-emerald-50 ${isPrint ? 'p-2' : 'p-4'} rounded-2xl border border-emerald-100 text-center shadow-sm`}>
            <div className="text-emerald-500 mb-1 flex justify-center"><BarChart3 size={isPrint ? 20 : 28} /></div>
            <div className={`${isPrint ? 'text-2xl' : 'text-3xl'} font-black text-emerald-700`}>{totalEvaluations}</div>
            <div className={`${isPrint ? 'text-[10px]' : 'text-xs'} font-bold text-emerald-600 mt-1`}>การประเมินรวม (ครั้ง)</div>
          </div>
          <div className={`bg-rose-50 ${isPrint ? 'p-2' : 'p-4'} rounded-2xl border border-rose-100 text-center shadow-sm`}>
            <div className="text-rose-500 mb-1 flex justify-center"><AlertCircle size={isPrint ? 20 : 28} /></div>
            <div className={`${isPrint ? 'text-2xl' : 'text-3xl'} font-black text-rose-700`}>{uniqueRiskUsers.size}</div>
            <div className={`${isPrint ? 'text-[10px]' : 'text-xs'} font-bold text-rose-600 mt-1`}>พบกลุ่มเสี่ยง (คน)</div>
          </div>
          <div className={`bg-purple-50 ${isPrint ? 'p-2' : 'p-4'} rounded-2xl border border-purple-100 text-center shadow-sm`}>
            <div className="text-purple-500 mb-1 flex justify-center"><TrendingUp size={isPrint ? 20 : 28} /></div>
            <div className={`${isPrint ? 'text-2xl' : 'text-3xl'} font-black text-purple-700`}>{riskPercentage}%</div>
            <div className={`${isPrint ? 'text-[10px]' : 'text-xs'} font-bold text-purple-600 mt-1`}>สัดส่วนกลุ่มเสี่ยง</div>
          </div>
        </div>"""

if old_kpis in content:
    content = content.replace(old_kpis, new_kpis)
    
    # Replace interpretation fonts
    content = content.replace('<div className="mt-4 p-4 bg-indigo-50/50 rounded-2xl border border-indigo-100">\n              <p className="text-sm font-medium text-indigo-800">{st5PieInterpretation}</p>', '<div className={`mt-4 p-4 bg-indigo-50/50 rounded-2xl border border-indigo-100 ${isPrint ? \'!p-2 !mt-2\' : \'\'}`}>\n              <p className={`${isPrint ? \'text-xs\' : \'text-sm\'} font-medium text-indigo-800`}>{st5PieInterpretation}</p>')
    content = content.replace('<div className="mt-4 p-4 bg-teal-50/50 rounded-2xl border border-teal-100">\n              <p className="text-sm font-medium text-teal-800">{barInterpretation}</p>', '<div className={`mt-4 p-4 bg-teal-50/50 rounded-2xl border border-teal-100 ${isPrint ? \'!p-2 !mt-2\' : \'\'}`}>\n              <p className={`${isPrint ? \'text-xs\' : \'text-sm\'} font-medium text-teal-800`}>{barInterpretation}</p>')
    
    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced KPIs!")
else:
    print("KPIs Not found")
