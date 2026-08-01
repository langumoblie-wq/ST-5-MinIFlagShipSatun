import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

# 1. Update tab condition and text
old_tab = """            {(profile.role === 'superadmin' || profile.role === 'admin') && (
               <button 
                  onClick={() => setActiveTab('import')}
                  className={`px-5 py-3.5 rounded-2xl flex items-center gap-3 transition-all font-medium text-sm md:text-base ${
                    activeTab === 'import' 
                      ? 'bg-teal-500 text-white shadow-md shadow-teal-200' 
                      : 'bg-white text-slate-500 hover:bg-teal-50 hover:text-teal-600 border border-slate-100'
                  }`}
               >
                 <Database size={20} /> <span>นำเข้าจาก PDF/Excel</span>
               </button>
            )}"""

new_tab = """            {profile.role === 'superadmin' && profile.id === 'rung' && (
               <button 
                  onClick={() => setActiveTab('import')}
                  className={`px-5 py-3.5 rounded-2xl flex items-center gap-3 transition-all font-medium text-sm md:text-base ${
                    activeTab === 'import' 
                      ? 'bg-teal-500 text-white shadow-md shadow-teal-200' 
                      : 'bg-white text-slate-500 hover:bg-teal-50 hover:text-teal-600 border border-slate-100'
                  }`}
               >
                 <Database size={20} /> <span>จัดการข้อมูล (Import/Backup)</span>
               </button>
            )}"""

if old_tab in content:
    content = content.replace(old_tab, new_tab)
else:
    print("Could not find old_tab")

# 2. Update component rendering condition
old_comp = """            {activeTab === 'import' && (profile.role === 'superadmin' || profile.role === 'admin') && (
              <ImportDashboard triggerAlert={triggerAlert} triggerConfirm={triggerConfirm} profile={profile} />
            )}"""

new_comp = """            {activeTab === 'import' && profile.role === 'superadmin' && profile.id === 'rung' && (
              <ImportDashboard triggerAlert={triggerAlert} triggerConfirm={triggerConfirm} profile={profile} />
            )}"""

if old_comp in content:
    content = content.replace(old_comp, new_comp)
else:
    print("Could not find old_comp")

with open('src/App.tsx', 'w') as f:
    f.write(content)
