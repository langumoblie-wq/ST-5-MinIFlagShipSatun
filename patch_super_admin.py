import re

with open('src/App.tsx', 'r') as f:
    code = f.read()

old_super = """function SuperAdminDashboard({ users, st5Data, behaviorData, profile, triggerAlert, triggerConfirm }) {"""
new_super = """function SuperAdminDashboard({ users, st5Data, behaviorData, profile, triggerAlert, triggerConfirm, triggerDownloadConsentPdf }) {"""

code = code.replace(old_super, new_super)

old_row_actions = """                  <td className="p-4 text-right">
                    {(u.role === 'user' || u.role === 'admin') ? (
                      <div className="flex items-center justify-end gap-2">
                        <button onClick={() => toggleStatus(u.id, u.status, u.name)} className={`${u.status === 'suspended' ? 'text-emerald-500 hover:bg-emerald-50' : 'text-amber-500 hover:bg-amber-50'} px-3 py-1.5 rounded-lg text-xs font-bold transition`}>
                          {u.status === 'suspended' ? 'ปลดระงับ' : 'ระงับ'}
                        </button>"""

new_row_actions = """                  <td className="p-4 text-right">
                    {(u.role === 'user' || u.role === 'admin') ? (
                      <div className="flex items-center justify-end gap-2">
                        <button onClick={() => triggerDownloadConsentPdf(u)} className="text-purple-500 hover:bg-purple-50 px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1">
                           <Download size={12}/> PDF
                        </button>
                        <button onClick={() => toggleStatus(u.id, u.status, u.name)} className={`${u.status === 'suspended' ? 'text-emerald-500 hover:bg-emerald-50' : 'text-amber-500 hover:bg-amber-50'} px-3 py-1.5 rounded-lg text-xs font-bold transition`}>
                          {u.status === 'suspended' ? 'ปลดระงับ' : 'ระงับ'}
                        </button>"""

code = code.replace(old_row_actions, new_row_actions)

with open('src/App.tsx', 'w') as f:
    f.write(code)
print("Updated SuperAdminDashboard!")
