import re

with open('src/App.tsx', 'r') as f:
    code = f.read()

old_code = """  const deleteUser = (uid, name) => {
    triggerConfirm(`ลบผู้ใช้ "${name}" ออกจากระบบถาวร ยืนยันหรือไม่?`, async () => {, 'danger')
      await deleteDoc(doc(db, 'artifacts', appId, 'public', 'data', 'users', uid));
      syncToGoogleSheet('DELETE_USER', { uid });
      triggerAlert('ลบข้อมูลผู้ใช้งานเรียบร้อยแล้วค่ะ', 'success');
    });
  };"""

new_code = """  const deleteUser = (uid, name) => {
    triggerConfirm(`ลบผู้ใช้ "${name}" ออกจากระบบถาวร ยืนยันหรือไม่?`, async () => {
      await deleteDoc(doc(db, 'artifacts', appId, 'public', 'data', 'users', uid));
      syncToGoogleSheet('DELETE_USER', { uid });
      triggerAlert('ลบข้อมูลผู้ใช้งานเรียบร้อยแล้วค่ะ', 'success');
    }, 'danger');
  };"""

if old_code in code:
    code = code.replace(old_code, new_code)
    with open('src/App.tsx', 'w') as f:
        f.write(code)
    print("Fixed deleteUser")
else:
    print("Could not find bad deleteUser")
