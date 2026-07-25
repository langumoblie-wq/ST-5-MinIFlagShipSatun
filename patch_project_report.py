import sys
with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add PieChart to imports if not there (it is there, I checked earlier)
# import { ... PieChart, ... } 

# Add menu item
menu_target = """            {(profile.role === 'admin' || profile.role === 'superadmin') && profile.status === 'approved' && (
               <button 
                  onClick={() => setActiveTab('analytics')}"""

menu_replacement = """            {(profile.role === 'admin' || profile.role === 'superadmin') && profile.status === 'approved' && (
               <>
               <button 
                  onClick={() => setActiveTab('project_report')}
                  className={`px-5 py-3.5 rounded-2xl flex items-center gap-3 transition-all font-medium text-sm md:text-base ${
                    activeTab === 'project_report' 
                      ? 'bg-blue-500 text-white shadow-md shadow-blue-200' 
                      : 'bg-white text-slate-500 hover:bg-blue-50 hover:text-blue-500 border border-slate-100'
                  }`}
               >
                 <PieChart size={20} /> <span>สรุปผลและติดตามโครงการ</span>
               </button>
               <button 
                  onClick={() => setActiveTab('analytics')}"""

if menu_target in content:
    content = content.replace(menu_target, menu_replacement)
    print("Menu item patched")
else:
    print("Menu item NOT found")

content_target = """            {activeTab === 'analytics' && profile.role === 'superadmin' && (
              <ExecutiveAnalyticsDashboard users={usersList} st5Data={st5Data} behaviorData={behaviorData} profile={profile} />
            )}"""

content_replacement = """            {activeTab === 'analytics' && profile.role === 'superadmin' && (
              <ExecutiveAnalyticsDashboard users={usersList} st5Data={st5Data} behaviorData={behaviorData} profile={profile} />
            )}
            {activeTab === 'project_report' && (profile.role === 'admin' || profile.role === 'superadmin') && (
              <ProjectReportDashboard users={usersList} st5Data={st5Data} behaviorData={behaviorData} profile={profile} />
            )}"""

if content_target in content:
    content = content.replace(content_target, content_replacement)
    print("Content area patched")
else:
    print("Content area NOT found")

with open('src/App.tsx', 'w') as f:
    f.write(content)
