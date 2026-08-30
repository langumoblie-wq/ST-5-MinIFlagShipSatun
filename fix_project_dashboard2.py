import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_code = """function ProjectReportDashboard({ users, st5Data, behaviorData, profile }) {
  
  const [selectedAffiliation, setSelectedAffiliation] = useState('all');
  const [expandedRows, setExpandedRows] = useState({});
  
  

  
  const affiliations = Array.from(new Set(users.filter(u => ['student', 'community'].includes(u.accountType) || u.role === 'user').map(u => u.affiliation).filter(Boolean)));
  
  const getStats = (affil) => {
    let studentsInAffil = users.filter(u => ['student', 'community'].includes(u.accountType) || u.role === 'user');
    if (affil !== 'all') {
      studentsInAffil = studentsInAffil.filter(u => u.affiliation === affil);
    }"""

new_code = """function ProjectReportDashboard({ users, st5Data, behaviorData, profile }) {
  
  const [selectedAffiliation, setSelectedAffiliation] = useState(profile.role === 'superadmin' ? 'all' : profile.affiliation);
  const [expandedRows, setExpandedRows] = useState({});
  
  const baseStudents = users.filter(u => (['student', 'community'].includes(u.accountType) || u.role === 'user') && (profile.role === 'superadmin' || u.affiliation === profile.affiliation));
  
  const affiliations = Array.from(new Set(baseStudents.map(u => u.affiliation).filter(Boolean)));
  
  const getStats = (affil) => {
    let studentsInAffil = baseStudents;
    if (affil !== 'all') {
      studentsInAffil = studentsInAffil.filter(u => u.affiliation === affil);
    }"""

# A more robust regex replacement:
content = re.sub(
    r"const \[selectedAffiliation, setSelectedAffiliation\] = useState\('all'\);.*?const getStats = \(affil\) => \{.*?studentsInAffil = studentsInAffil\.filter\(u => u\.affiliation === affil\);\n    \}",
    """const [selectedAffiliation, setSelectedAffiliation] = useState(profile.role === 'superadmin' ? 'all' : profile.affiliation);
  const [expandedRows, setExpandedRows] = useState({});
  
  const baseStudents = users.filter(u => (['student', 'community'].includes(u.accountType) || u.role === 'user') && (profile.role === 'superadmin' || u.affiliation === profile.affiliation));
  
  const affiliations = Array.from(new Set(baseStudents.map(u => u.affiliation).filter(Boolean)));
  
  const getStats = (affil) => {
    let studentsInAffil = baseStudents;
    if (affil !== 'all') {
      studentsInAffil = studentsInAffil.filter(u => u.affiliation === affil);
    }""",
    content,
    flags=re.DOTALL
)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

