import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

target = """                                      <td className="p-4 md:p-5">
                                          <button onClick={() => toggleRow(affil)} className="flex items-center gap-2 text-sm font-black text-slate-800 no-print w-full text-left">
                                              {isExpanded ? <ChevronDown size={16} className="text-slate-400" /> : <ChevronRight size={16} className="text-slate-400" />}
                                              {affil} 
                                              <span className="text-[9px] text-blue-500 font-medium bg-blue-50 px-2 py-0.5 rounded-full opacity-0 group-hover:opacity-100 transition-opacity ml-2 hidden md:inline-block">(คลิกดูรายละเอียด)</span>
                                          </button>
                                          <div className="print-only font-black text-slate-800 text-sm hidden">
                                              {affil}
                                          </div>
                                      </td>"""

replacement = """                                      <td className="p-4 md:p-5">
                                          <button onClick={() => toggleRow(affil)} className="flex items-center gap-2 text-sm font-black text-slate-800 w-full text-left">
                                              <span className="no-print">
                                                  {isExpanded ? <ChevronDown size={16} className="text-slate-400" /> : <ChevronRight size={16} className="text-slate-400" />}
                                              </span>
                                              {affil} 
                                              <span className="no-print text-[9px] text-blue-500 font-medium bg-blue-50 px-2 py-0.5 rounded-full opacity-0 group-hover:opacity-100 transition-opacity ml-2 hidden md:inline-block">(คลิกดูรายละเอียด)</span>
                                          </button>
                                      </td>"""

if target in content:
    content = content.replace(target, replacement)
    with open('src/App.tsx', 'w') as f:
        f.write(content)
    print("Row fixed")
else:
    print("Target not found")
