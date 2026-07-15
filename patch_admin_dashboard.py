import re

with open('src/App.tsx', 'r') as f:
    code = f.read()

old_code = """function AdminDashboard({ users, st5Data, behaviorData, profile, triggerAlert, triggerConfirm, triggerDownloadConsentPdf }) {
  const [selectedUserId, setSelectedUserId] = useState(null);
  const students = users.filter(u => ['student', 'community', 'teacher'].includes(u.accountType) && u.affiliation === profile.affiliation);

  const selectedUser = users.find(u => u.id === selectedUserId);

  if (selectedUser) return <AdminStudentDetail student={selectedUser} st5History={st5Data.filter(d => d.uid === selectedUser.id || d.userId === selectedUser.id)} behaviorHistory={behaviorData.filter(d => d.targetUid === selectedUser.id)} onBack={() => setSelectedUserId(null)} triggerAlert={triggerAlert} triggerConfirm={triggerConfirm} triggerDownloadConsentPdf={triggerDownloadConsentPdf} />;

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-[2rem] shadow-sm border border-slate-100">
        <h2 className="text-2xl font-black text-slate-800 flex items-center gap-2"><ClipboardList className="text-purple-400"/> รายชื่อในความดูแล</h2>
        <div className="mt-2 inline-flex items-center gap-2 bg-purple-50 px-3 py-1.5 rounded-full border border-purple-100">
           <span className="text-xs font-bold text-purple-400">สังกัด</span>
           <span className="text-sm font-semibold text-purple-700">{profile.affiliation}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
        {students.map(student => (
          <div key={student.id} onClick={() => setSelectedUserId(student.id)} 
               className="bg-white p-5 md:p-6 rounded-[2rem] shadow-sm border border-slate-100 flex justify-between items-center hover:shadow-lg hover:shadow-purple-100/50 hover:border-purple-200 transition-all cursor-pointer group transform hover:-translate-y-1">
            <div className="flex items-center gap-4 overflow-hidden">
              <div className="w-14 h-14 shrink-0 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full flex items-center justify-center text-purple-500 font-black text-xl shadow-inner border border-white">
                {student.name.charAt(0)}
              </div>
              <div className="min-w-0">
                <p className="font-bold text-slate-700 truncate text-base group-hover:text-purple-600 transition">{student.name}</p>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-[10px] font-bold bg-slate-100 text-slate-500 px-2 py-0.5 rounded-md">{student.accountType === 'student' ? 'นักเรียน' : student.accountType === 'teacher' ? 'ครู' : 'ชุมชน'}</span>
                </div>
              </div>
            </div>
            <div className="w-10 h-10 shrink-0 bg-slate-50 rounded-full flex items-center justify-center text-slate-300 group-hover:bg-purple-500 group-hover:text-white transition-all shadow-sm">
              <ChevronRight size={20} strokeWidth={3}/>
            </div>
          </div>
        ))}
        {students.length === 0 && (
          <div className="col-span-full bg-white p-12 rounded-[2rem] text-center border-2 border-dashed border-slate-200">
            <Users className="mx-auto text-slate-200 mb-4" size={48} />
            <p className="text-slate-500 font-medium">ยังไม่มีรายชื่อผู้ใช้งานในสังกัดนี้</p>
          </div>
        )}
      </div>
    </div>
  );
}"""

new_code = """function AdminDashboard({ users, st5Data, behaviorData, profile, triggerAlert, triggerConfirm, triggerDownloadConsentPdf }) {
  const [selectedUserId, setSelectedUserId] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  
  // กรองผู้ใช้งานในสังกัด และจัดเรียงตามชื่อ ก-ฮ
  const students = users
    .filter(u => ['student', 'community', 'teacher'].includes(u.accountType) && u.affiliation === profile.affiliation)
    .sort((a, b) => a.name.localeCompare(b.name, 'th'));

  // ค้นหา
  const filteredStudents = students.filter(u => 
    u.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
    (u.id && u.id.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const selectedUser = users.find(u => u.id === selectedUserId);

  return (
    <div className="flex flex-col lg:flex-row gap-6 lg:h-[calc(100vh-160px)]">
      {/* 1. Sidebar แสดงรายชื่อ */}
      <div className={`w-full lg:w-[400px] flex-shrink-0 flex flex-col gap-4 ${selectedUser ? 'hidden lg:flex' : 'flex'}`}>
        <div className="bg-white p-5 rounded-[2rem] shadow-sm border border-slate-100 shrink-0">
          <h2 className="text-xl font-black text-slate-800 flex items-center gap-2 mb-3"><ClipboardList className="text-purple-400"/> รายชื่อในความดูแล</h2>
          <div className="flex flex-col gap-3">
             <div className="inline-flex items-center gap-2 bg-purple-50 px-3 py-1.5 rounded-full border border-purple-100 self-start">
               <span className="text-[10px] font-bold text-purple-400">สังกัด</span>
               <span className="text-xs font-semibold text-purple-700">{profile.affiliation}</span>
             </div>
             
             {/* Filter Input */}
             <div className="relative mt-2">
                <input 
                  type="text" 
                  placeholder="ค้นหารายชื่อ หรือ ID..." 
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-2xl text-sm focus:ring-4 focus:ring-purple-500/20 focus:border-purple-400 outline-none transition-all font-medium text-slate-700"
                />
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
             </div>
          </div>
        </div>

        {/* List of Users */}
        <div className="flex-1 overflow-y-auto hide-scrollbar space-y-3 pb-6">
          {filteredStudents.map(student => {
            const st5Count = st5Data.filter(d => d.uid === student.id || d.userId === student.id).length;
            const behCount = behaviorData.filter(d => d.targetUid === student.id).length;
            const isSelected = selectedUserId === student.id;

            return (
              <div key={student.id} onClick={() => setSelectedUserId(student.id)} 
                   className={`p-4 rounded-[2rem] shadow-sm border flex justify-between items-center hover:shadow-md transition-all cursor-pointer group transform hover:-translate-y-0.5 ${isSelected ? 'bg-purple-50 border-purple-200 ring-2 ring-purple-400/20' : 'bg-white border-slate-100 hover:border-purple-200'}`}>
                <div className="flex items-center gap-4 overflow-hidden">
                  <div className={`w-12 h-12 shrink-0 rounded-full flex items-center justify-center font-black text-lg shadow-inner border border-white transition-colors ${isSelected ? 'bg-purple-500 text-white' : 'bg-gradient-to-br from-purple-100 to-pink-100 text-purple-500'}`}>
                    {student.name.charAt(0)}
                  </div>
                  <div className="min-w-0">
                    <p className={`font-bold truncate text-sm transition ${isSelected ? 'text-purple-700' : 'text-slate-700 group-hover:text-purple-600'}`}>{student.name}</p>
                    <div className="flex items-center gap-1.5 mt-1.5 flex-wrap">
                      <span className="text-[9px] font-bold bg-slate-100 text-slate-500 px-1.5 py-0.5 rounded-md">
                        {student.accountType === 'student' ? 'นักเรียน' : student.accountType === 'teacher' ? 'ครู' : 'ชุมชน'}
                      </span>
                      {st5Count > 0 && <span className="text-[9px] font-bold bg-teal-50 text-teal-600 px-1.5 py-0.5 rounded-md border border-teal-100">ST-5: {st5Count}</span>}
                      {behCount > 0 && <span className="text-[9px] font-bold bg-orange-50 text-orange-600 px-1.5 py-0.5 rounded-md border border-orange-100">พฤติกรรม: {behCount}</span>}
                    </div>
                  </div>
                </div>
                <div className={`w-8 h-8 shrink-0 rounded-full flex items-center justify-center transition-all shadow-sm ${isSelected ? 'bg-purple-500 text-white' : 'bg-slate-50 text-slate-300 group-hover:bg-purple-400 group-hover:text-white'}`}>
                  <ChevronRight size={18} strokeWidth={3}/>
                </div>
              </div>
            );
          })}
          {filteredStudents.length === 0 && (
            <div className="bg-white p-8 rounded-[2rem] text-center border-2 border-dashed border-slate-200">
              <Users className="mx-auto text-slate-300 mb-3" size={36} />
              <p className="text-slate-500 font-medium text-sm">ไม่พบรายชื่อที่ค้นหา</p>
            </div>
          )}
        </div>
      </div>

      {/* 2. Main Content Area */}
      <div className={`w-full lg:flex-1 overflow-y-auto hide-scrollbar bg-slate-50/50 rounded-[2.5rem] border border-slate-100 relative ${!selectedUser ? 'hidden lg:flex items-center justify-center' : 'block'}`}>
        {selectedUser ? (
          <div className="p-4 md:p-6 lg:p-8 min-h-full">
            <AdminStudentDetail 
              student={selectedUser} 
              st5History={st5Data.filter(d => d.uid === selectedUser.id || d.userId === selectedUser.id)} 
              behaviorHistory={behaviorData.filter(d => d.targetUid === selectedUser.id)} 
              onBack={() => setSelectedUserId(null)} 
              triggerAlert={triggerAlert} 
              triggerConfirm={triggerConfirm} 
              triggerDownloadConsentPdf={triggerDownloadConsentPdf} 
            />
          </div>
        ) : (
          <div className="text-center p-8">
             <div className="w-24 h-24 bg-white rounded-full flex items-center justify-center mx-auto mb-6 shadow-sm border border-slate-100">
               <UserSquare2 size={48} className="text-slate-300" strokeWidth={1.5} />
             </div>
             <h3 className="text-xl font-black text-slate-700 mb-2">เลือกรายชื่อในความดูแล</h3>
             <p className="text-slate-500 font-medium text-sm max-w-sm mx-auto">คลิกเลือกนักเรียนหรือผู้ใช้งานจากรายชื่อด้านซ้าย เพื่อดูรายงานผลสุขภาพจิตและประวัติพฤติกรรมอย่างละเอียด</p>
          </div>
        )}
      </div>
    </div>
  );
}"""

if old_code in code:
    code = code.replace(old_code, new_code)
    with open('src/App.tsx', 'w') as f:
        f.write(code)
    print("Replaced AdminDashboard")
else:
    print("Could not find old_code")
