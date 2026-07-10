import re

with open('src/App.tsx', 'r') as f:
    code = f.read()

old_dash_start = """function UserDashboard({ users, profile, st5Data, behaviorData, triggerAlert, triggerConfirm }) {
  const [showST5, setShowST5] = useState(false);"""

new_dash_start = """function UserDashboard({ users, profile, st5Data, behaviorData, triggerAlert, triggerConfirm }) {
  const [showST5, setShowST5] = useState(false);
  const myAdmins = users?.filter(u => u.role === 'admin' && u.affiliation === profile.affiliation && u.status === 'approved') || [];
  const projectMentors = users?.filter(u => u.role === 'superadmin') || [];
"""

code = code.replace(old_dash_start, new_dash_start)

old_html = """          <p className="text-slate-500 text-sm mt-1">ยินดีต้อนรับกลับมานะ สำรวจสุขภาพใจของคุณกันเถอะ</p>
        </div>"""

new_html = """          <p className="text-slate-500 text-sm mt-1">ยินดีต้อนรับกลับมานะ สำรวจสุขภาพใจของคุณกันเถอะ</p>
        </div>
        
        <div className="flex-1 w-full md:w-auto mt-4 md:mt-0 flex flex-col md:flex-row gap-3">
           {myAdmins.length > 0 && (
             <div className="bg-sky-50 border border-sky-100 p-3 rounded-2xl flex-1">
                <p className="text-[10px] font-bold text-sky-600 mb-1">ครู/ผู้รับผิดชอบ (Admin)</p>
                <div className="flex flex-wrap gap-2">
                  {myAdmins.map(a => (
                     <span key={a.id} className="text-xs font-medium text-slate-700 bg-white px-2 py-1 rounded-lg border border-sky-100">{a.name}</span>
                  ))}
                </div>
             </div>
           )}
           {projectMentors.length > 0 && (
             <div className="bg-purple-50 border border-purple-100 p-3 rounded-2xl flex-1">
                <p className="text-[10px] font-bold text-purple-600 mb-1">พี่เลี้ยงโครงการ</p>
                <div className="flex flex-wrap gap-2">
                  {projectMentors.map(m => (
                     <span key={m.id} className="text-xs font-medium text-slate-700 bg-white px-2 py-1 rounded-lg border border-purple-100">{m.name}</span>
                  ))}
                </div>
             </div>
           )}
        </div>"""

code = code.replace(old_html, new_html)

with open('src/App.tsx', 'w') as f:
    f.write(code)
print("Updated UserDashboard!")
