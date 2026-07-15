import re

with open('src/App.tsx', 'r') as f:
    code = f.read()

old_code = """function AdminStudentDetail({ student, st5History, behaviorHistory, onBack, triggerAlert, triggerConfirm, triggerDownloadConsentPdf }) {
  const [showBehaviorForm, setShowBehaviorForm] = useState(false);
  const [editingBehavior, setEditingBehavior] = useState(null);
  const [viewingSt5Result, setViewingSt5Result] = useState(null); 
  const [viewingBehaviorResult, setViewingBehaviorResult] = useState(null);

  const saveSuggestion = async (docId, text) => {
    await updateDoc(doc(db, 'artifacts', appId, 'public', 'data', 'st5', docId), { suggestion: text });
    triggerAlert('บันทึกคำแนะนำความห่วงใยเรียบร้อยแล้วค่ะ ✦', 'success');
  };"""

new_code = """function AdminStudentDetail({ student, st5History, behaviorHistory, onBack, triggerAlert, triggerConfirm, triggerDownloadConsentPdf }) {
  const [showBehaviorForm, setShowBehaviorForm] = useState(false);
  const [editingBehavior, setEditingBehavior] = useState(null);
  const [viewingSt5Result, setViewingSt5Result] = useState(null); 
  const [viewingBehaviorResult, setViewingBehaviorResult] = useState(null);
  const [editingUser, setEditingUser] = useState(false);

  const handleSaveUser = async (uid, updatedData) => {
    await updateDoc(doc(db, 'artifacts', appId, 'public', 'data', 'users', uid), updatedData);
    syncToGoogleSheet('EDIT_USER', { uid, ...updatedData });
    setEditingUser(false);
    triggerAlert('อัปเดตข้อมูลผู้ใช้งานสำเร็จ ✦', 'success');
  };

  const handleDeleteUser = () => {
    triggerConfirm(`ลบผู้ใช้ "${student.name}" ออกจากระบบถาวร ยืนยันหรือไม่?`, async () => {
      await deleteDoc(doc(db, 'artifacts', appId, 'public', 'data', 'users', student.id));
      syncToGoogleSheet('DELETE_USER', { uid: student.id });
      triggerAlert('ลบข้อมูลผู้ใช้งานเรียบร้อยแล้วค่ะ', 'success');
      onBack();
    }, 'danger');
  };

  const saveSuggestion = async (docId, text) => {
    await updateDoc(doc(db, 'artifacts', appId, 'public', 'data', 'st5', docId), { suggestion: text });
    triggerAlert('บันทึกคำแนะนำความห่วงใยเรียบร้อยแล้วค่ะ ✦', 'success');
  };"""

if old_code in code:
    code = code.replace(old_code, new_code)
    print("Patched AdminStudentDetail state and logic")
else:
    print("Could not find AdminStudentDetail head")
    
with open('src/App.tsx', 'w') as f:
    f.write(code)
