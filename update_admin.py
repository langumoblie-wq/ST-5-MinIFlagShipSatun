import re

with open('src/App.tsx', 'r') as f:
    code = f.read()

# Fix AdminDashboard props
old_admin_dash = """function AdminDashboard({ users, st5Data, behaviorData, profile, triggerAlert, triggerConfirm }) {
  const [selectedUser, setSelectedUser] = useState(null);
  const students = users.filter(u => ['student', 'community', 'teacher'].includes(u.accountType) && u.affiliation === profile.affiliation);

  if (selectedUser) return <AdminStudentDetail student={selectedUser} st5History={st5Data.filter(d => d.uid === selectedUser.id || d.userId === selectedUser.id)} behaviorHistory={behaviorData.filter(d => d.targetUid === selectedUser.id)} onBack={() => setSelectedUser(null)} triggerAlert={triggerAlert} triggerConfirm={triggerConfirm} />;"""

new_admin_dash = """function AdminDashboard({ users, st5Data, behaviorData, profile, triggerAlert, triggerConfirm, triggerDownloadConsentPdf }) {
  const [selectedUser, setSelectedUser] = useState(null);
  const students = users.filter(u => ['student', 'community', 'teacher'].includes(u.accountType) && u.affiliation === profile.affiliation);

  if (selectedUser) return <AdminStudentDetail student={selectedUser} st5History={st5Data.filter(d => d.uid === selectedUser.id || d.userId === selectedUser.id)} behaviorHistory={behaviorData.filter(d => d.targetUid === selectedUser.id)} onBack={() => setSelectedUser(null)} triggerAlert={triggerAlert} triggerConfirm={triggerConfirm} triggerDownloadConsentPdf={triggerDownloadConsentPdf} />;"""

code = code.replace(old_admin_dash, new_admin_dash)

# Fix AdminStudentDetail
old_student_detail_start = """function AdminStudentDetail({ student, st5History, behaviorHistory, onBack, triggerAlert, triggerConfirm }) {
  const [showBehaviorForm, setShowBehaviorForm] = useState(false);
  const [isDownloadingPdf, setIsDownloadingPdf] = useState(false);

  const downloadConsentPdf = async () => {
    setIsDownloadingPdf(true);
    const element = document.getElementById(`consent-pdf-${student.id}`);
    if (!element) {
      setIsDownloadingPdf(false);
      return;
    }
    const originalStyles = {
      position: element.style.position,
      left: element.style.left,
      top: element.style.top,
      width: element.style.width,
    };
    element.style.position = 'absolute';
    element.style.left = '0';
    element.style.top = '0';
    element.style.width = '800px';
    element.style.zIndex = '-9999';
    try {
      const dataUrl = await toPng(element, { quality: 0.95, pixelRatio: 2, backgroundColor: '#ffffff' });
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4'
      });
      const imgProps = pdf.getImageProperties(dataUrl);
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
      
      pdf.addImage(dataUrl, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`ConsentForm_${student.name}.pdf`);
      triggerAlert('โหลด Consent Form สำเร็จ', 'success');
    } catch (err) {
      console.error(err);
      triggerAlert('เกิดข้อผิดพลาดในการสร้าง PDF', 'error');
    } finally {
      element.style.position = originalStyles.position;
      element.style.left = originalStyles.left;
      element.style.top = originalStyles.top;
      element.style.width = originalStyles.width;
      setIsDownloadingPdf(false);
    }
  };"""

new_student_detail_start = """function AdminStudentDetail({ student, st5History, behaviorHistory, onBack, triggerAlert, triggerConfirm, triggerDownloadConsentPdf }) {
  const [showBehaviorForm, setShowBehaviorForm] = useState(false);
  const [editingBehavior, setEditingBehavior] = useState(null);"""

code = code.replace(old_student_detail_start, new_student_detail_start)

# Fix AdminStudentDetail download button action and remove isDownloadingPdf
code = code.replace("downloadConsentPdf", "() => triggerDownloadConsentPdf(student)")
code = code.replace("disabled={isDownloadingPdf}", "")
code = code.replace("{isDownloadingPdf ? 'กำลังโหลด...' : 'โหลด Consent Form'}", "'โหลด Consent Form'")


# Remove the hidden div at the bottom of AdminStudentDetail
old_student_detail_end = """    <div className="max-w-6xl mx-auto space-y-6">
      <div className="absolute top-[-9999px] left-[-9999px] w-[800px] bg-white text-black overflow-hidden pointer-events-none">
         <div id={`consent-pdf-${student.id}`}>
           <ConsentDocument 
               name={student.name} 
               dateStr={student.createdAt ? new Date(student.createdAt).toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' }) : new Date().toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' })}
               hidePrintBtn={true}
               onPrint={() => {}}
           />
         </div>
      </div>"""

new_student_detail_end = """    <div className="max-w-6xl mx-auto space-y-6">"""

code = code.replace(old_student_detail_end, new_student_detail_end)


with open('src/App.tsx', 'w') as f:
    f.write(code)
print("Updated Admin dashboards!")
