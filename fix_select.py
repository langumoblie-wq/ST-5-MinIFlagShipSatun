import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_select = """         <div className="flex flex-wrap gap-3">
             <select 
                value={selectedAffiliation}
                onChange={(e) => setSelectedAffiliation(e.target.value)}
                className="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-xl px-4 py-2 font-medium min-w-[200px] outline-none focus:border-blue-300 transition-colors"
             >
                <option value="all">ทุกพื้นที่เป้าหมาย / สังกัด</option>
                {affiliations.map(aff => (
                    <option key={aff} value={aff}>{aff}</option>
                ))}
             </select>"""

new_select = """         <div className="flex flex-wrap gap-3">
             {profile.role === 'superadmin' ? (
                 <select 
                    value={selectedAffiliation}
                    onChange={(e) => setSelectedAffiliation(e.target.value)}
                    className="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-xl px-4 py-2 font-medium min-w-[200px] outline-none focus:border-blue-300 transition-colors"
                 >
                    <option value="all">ทุกพื้นที่เป้าหมาย / สังกัด</option>
                    {affiliations.map(aff => (
                        <option key={aff} value={aff}>{aff}</option>
                    ))}
                 </select>
             ) : (
                 <div className="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-xl px-4 py-2 font-medium min-w-[200px] flex items-center">
                    {profile.affiliation}
                 </div>
             )}"""

if old_select in content:
    content = content.replace(old_select, new_select)
    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced!")
else:
    print("Not found")

