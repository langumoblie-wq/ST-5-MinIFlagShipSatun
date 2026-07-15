import re

with open('src/App.tsx', 'r') as f:
    code = f.read()

old_header = """  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <button onClick={onBack} className="text-slate-400 hover:text-purple-600 mb-2 flex items-center gap-2 font-bold transition bg-white px-4 py-2 rounded-full shadow-sm border border-slate-100 w-fit text-sm">
        <ChevronRight className="rotate-180" size={16}/> กลับไปหน้ารายชื่อ
      </button>
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 bg-white p-6 md:p-8 rounded-[2.5rem] shadow-sm border border-slate-100">
        <div className="flex items-center gap-5">
           <div className="w-20 h-20 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-full flex items-center justify-center text-purple-600 font-black text-3xl shadow-inner border-2 border-white">
              {student.name.charAt(0)}
           </div>
           <div>
             <h2 className="text-2xl md:text-3xl font-black text-slate-800 tracking-tight">{student.name}</h2>
             <p className="text-slate-500 text-sm mt-1 font-medium bg-slate-50 px-3 py-1 rounded-lg inline-block">ID: {student.id}</p>
           </div>
        </div>"""

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
      </button>
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 bg-white p-6 md:p-8 rounded-[2.5rem] shadow-sm border border-slate-100">
        <div className="flex items-center gap-5">
           <div className="w-20 h-20 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-full flex items-center justify-center text-purple-600 font-black text-3xl shadow-inner border-2 border-white">
              {student.name.charAt(0)}
           </div>
           <div>
             <h2 className="text-2xl md:text-3xl font-black text-slate-800 tracking-tight">{student.name}</h2>
             <div className="flex items-center gap-2 mt-2 flex-wrap">
                <p className="text-slate-500 text-sm font-medium bg-slate-50 px-3 py-1 rounded-lg">ID: {student.id}</p>
                <button onClick={() => setEditingUser(true)} className="text-sky-500 hover:bg-sky-50 px-3 py-1 rounded-lg text-xs font-bold transition">แก้ไขข้อมูล</button>
                <button onClick={handleDeleteUser} className="text-rose-500 hover:text-white hover:bg-rose-500 px-3 py-1 rounded-lg text-xs font-bold transition border border-rose-100 hover:border-rose-500">ลบข้อมูลผู้ใช้</button>
             </div>
           </div>
        </div>"""

if old_header in code:
    code = code.replace(old_header, new_header)
    print("Patched header")
else:
    print("Could not find header")

with open('src/App.tsx', 'w') as f:
    f.write(code)
