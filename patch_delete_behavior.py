import re

with open('src/App.tsx', 'r') as f:
    code = f.read()

old_code = """  const deleteBehavior = (behId, timestamp) => {
    triggerConfirm('ยืนยันการลบประวัติประเมินพฤติกรรมนี้ออกจากระบบ?', async () => {
      await deleteDoc(doc(db, 'artifacts', appId, 'public', 'data', 'behaviors', behId));
      syncToGoogleSheet('DELETE_BEHAVIOR', { targetName: student.name, timestamp: timestamp });
      triggerAlert('ลบประวัติพฤติกรรมเรียบร้อยแล้วค่ะ', 'success');
    });
  };"""

new_code = """  const deleteBehavior = (behId, timestamp) => {
    triggerConfirm('ยืนยันการลบประวัติประเมินพฤติกรรมนี้ออกจากระบบ?', async () => {
      await deleteDoc(doc(db, 'artifacts', appId, 'public', 'data', 'behaviors', behId));
      syncToGoogleSheet('DELETE_BEHAVIOR', { targetName: student.name, timestamp: timestamp });
      triggerAlert('ลบประวัติพฤติกรรมเรียบร้อยแล้วค่ะ', 'success');
    }, 'danger');
  };"""

if old_code in code:
    code = code.replace(old_code, new_code)
    print("Patched deleteBehavior")
else:
    print("Could not find deleteBehavior")

with open('src/App.tsx', 'w') as f:
    f.write(code)
