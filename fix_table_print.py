import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update renderTable definition
content = content.replace('const renderTable = () => {', 'const renderTable = (isPrint = false) => {')

# 2. Update renderTable usage in print section
content = content.replace('{renderTable()}', '{renderTable(isPrint)}')

# 3. Specifically fix the usage in the hidden print section
old_print_section = """           {/* Section 2: Table Data */}
           <div className="space-y-4">
             <h2 className="text-xl font-black text-blue-700 flex items-center gap-2 border-l-4 border-blue-500 pl-3">สถิติแยกตามหน่วยงาน (สุขภาพจิต)</h2>
             {renderTable(isPrint)}
           </div>"""
new_print_section = """           {/* Section 2: Table Data */}
           <div className="space-y-4">
             <h2 className="text-xl font-black text-blue-700 flex items-center gap-2 border-l-4 border-blue-500 pl-3">สถิติแยกตามหน่วยงาน (สุขภาพจิต)</h2>
             {renderTable(true)}
           </div>"""
content = content.replace(old_print_section, new_print_section)

# And fix the normal tab which should just be renderTable() (or isPrint is false by default)
old_normal_section = """         {reportTab === 'mental' && (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
               {renderTable(isPrint)}
            </div>
         )}"""
new_normal_section = """         {reportTab === 'mental' && (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
               {renderTable()}
            </div>
         )}"""
content = content.replace(old_normal_section, new_normal_section)

# 4. Update the overflow class inside renderTable
old_table_wrapper = '<div className="overflow-x-auto rounded-xl border border-slate-200 shadow-sm">'
new_table_wrapper = '<div className={`${isPrint ? \'\' : \'overflow-x-auto\'} rounded-xl border border-slate-200 shadow-sm`}>'
content = content.replace(old_table_wrapper, new_table_wrapper)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
