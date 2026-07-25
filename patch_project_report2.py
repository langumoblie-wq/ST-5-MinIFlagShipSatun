import sys
with open('src/App.tsx', 'r') as f:
    content = f.read()

content_target = """            {activeTab === 'analytics' && (profile.role === 'admin' || profile.role === 'superadmin') && (
              <ExecutiveAnalyticsDashboard users={usersList} st5Data={st5Data} behaviorData={behaviorData} profile={profile} />
            )}"""

content_replacement = """            {activeTab === 'analytics' && (profile.role === 'admin' || profile.role === 'superadmin') && (
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
