import re

with open('src/App.tsx', 'r') as f:
    code = f.read()

old_header = """  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <button onClick={onBack} className="text-slate-400 hover:text-purple-600 mb-2 flex items-center gap-2 font-bold transition bg-white px-4 py-2 rounded-full shadow-sm border border-slate-100 w-fit text-sm">
        <ChevronRight className="rotate-180" size={16}/> กลับไปหน้ารายชื่อ
      </button>"""

new_header = """  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {editingUser && (
        <EditUserModal 
          user={student} 
          onClose={() => setEditingUser(false)} 
          onSave={handleSaveUser} 
        />
      )}
      <button onClick={onBack} className="text-slate-400 hover:text-purple-600 mb-2 flex items-center gap-2 font-bold transition bg-white px-4 py-2 rounded-full shadow-sm border border-slate-100 w-fit text-sm">
        <ChevronRight className="rotate-180" size={16}/> กลับไปหน้ารายชื่อ
      </button>"""

if old_header in code:
    code = code.replace(old_header, new_header)
    print("Patched header top")
else:
    print("Could not find header top")


old_name = """           <div>
             <h2 className="text-2xl md:text-3xl font-black text-slate-800 tracking-tight">{student.name}</h2>
             <p className="text-slate-500 text-sm mt-1 font-medium bg-slate-50 px-3 py-1 rounded-lg inline-block">ID: {student.id}</p>
           </div>"""

new_name = """           <div>
             <h2 className="text-2xl md:text-3xl font-black text-slate-800 tracking-tight">{student.name}</h2>
             <div className="flex items-center gap-2 mt-2 flex-wrap">
                <p className="text-slate-500 text-sm font-medium bg-slate-50 px-3 py-1 rounded-lg">ID: {student.id}</p>
                <button onClick={() => setEditingUser(true)} className="text-sky-500 hover:bg-sky-50 px-3 py-1 rounded-lg text-xs font-bold transition">แก้ไขข้อมูล</button>
                <button onClick={handleDeleteUser} className="text-rose-500 hover:text-white hover:bg-rose-500 px-3 py-1 rounded-lg text-xs font-bold transition border border-rose-100 hover:border-rose-500">ลบข้อมูลผู้ใช้</button>
             </div>
           </div>"""

if old_name in code:
    code = code.replace(old_name, new_name)
    print("Patched name row")
else:
    print("Could not find name row")

with open('src/App.tsx', 'w') as f:
    f.write(code)
