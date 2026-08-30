import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_code = """  const [selectedAffiliation, setSelectedAffiliation] = useState('all');
  const [expandedRows, setExpandedRows] = useState({});
  
  

  

  const affiliations = Array.from(new Set(users.filter(u => ['student', 'community'].includes(u.accountType) || u.role === 'user').map(u => u.affiliation).filter(Boolean)));
  
  const getStats = (affil) => {
    let studentsInAffil = users.filter(u => ['student', 'community'].includes(u.accountType) || u.role === 'user');
    if (affil !== 'all') {
      studentsInAffil = studentsInAffil.filter(u => u.affiliation === affil);
    }"""

new_code = """  const [selectedAffiliation, setSelectedAffiliation] = useState(profile.role === 'superadmin' ? 'all' : profile.affiliation);
  const [expandedRows, setExpandedRows] = useState({});
  
  const baseStudents = users.filter(u => (['student', 'community'].includes(u.accountType) || u.role === 'user') && (profile.role === 'superadmin' || u.affiliation === profile.affiliation));

  const affiliations = Array.from(new Set(baseStudents.map(u => u.affiliation).filter(Boolean)));
  
  const getStats = (affil) => {
    let studentsInAffil = baseStudents;
    if (affil !== 'all') {
      studentsInAffil = studentsInAffil.filter(u => u.affiliation === affil);
    }"""

if old_code in content:
    content = content.replace(old_code, new_code)
    
    # Also fix the select dropdown in ProjectReportDashboard to be hidden/disabled if not superadmin?
    # Or just let them see only their own affiliation. Actually, they shouldn't see "all" if they are admin.
    
    # Let's write the whole file content to be safe.
    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed!")
else:
    print("Not found")
