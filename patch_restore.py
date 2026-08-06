import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

old_logic = """                                triggerConfirm(`คำเตือน: การกู้คืนข้อมูลจะนำข้อมูลจากไฟล์ (Users: ${data.users.length}, ST-5: ${data.st5.length}, Behaviors: ${data.behaviors.length}) เพิ่ม/ทับลงในระบบ ยืนยันหรือไม่?`, async () => {
                                    try {
                                        setIsImporting(true);
                                        // 1. Users
                                        for(const u of data.users) {
                                            const { id, ...rest } = u;
                                            await setDoc(doc(db, 'artifacts', appId, 'public', 'data', 'users', id), rest);
                                        }
                                        // 2. ST5
                                        for(const s of data.st5) {
                                            const { id, ...rest } = s;
                                            await setDoc(doc(db, 'artifacts', appId, 'public', 'data', 'st5', id), rest);
                                        }
                                        // 3. Behaviors
                                        for(const b of data.behaviors) {
                                            const { id, ...rest } = b;
                                            await setDoc(doc(db, 'artifacts', appId, 'public', 'data', 'behaviors', id), rest);
                                        }
                                        
                                        triggerAlert('กู้คืนข้อมูลเรียบร้อยแล้ว!', 'success');
                                    } catch(err) {
                                        triggerAlert('เกิดข้อผิดพลาดในการกู้คืนข้อมูล: ' + err.message, 'error');
                                    } finally {
                                        setIsImporting(false);
                                    }
                                }, 'danger');"""

new_logic = """                                triggerConfirm(`คำเตือน: การกู้คืนข้อมูลจะนำข้อมูลจากไฟล์ (Users: ${data.users.length}, ST-5: ${data.st5.length}, Behaviors: ${data.behaviors.length}) เพิ่ม/ทับลงในระบบ ยืนยันหรือไม่?`, async () => {
                                    try {
                                        const totalItems = data.users.length + data.st5.length + data.behaviors.length;
                                        setRestoreStatus({
                                            isRestoring: true,
                                            current: 0,
                                            total: totalItems,
                                            message: 'เริ่มต้นการกู้คืนข้อมูล...',
                                            finished: false,
                                            error: null
                                        });
                                        let currentCount = 0;

                                        // 1. Users
                                        for(const u of data.users) {
                                            const { id, ...rest } = u;
                                            await setDoc(doc(db, 'artifacts', appId, 'public', 'data', 'users', id), rest);
                                            currentCount++;
                                            setRestoreStatus(prev => ({...prev, current: currentCount, message: `กำลังกู้คืนข้อมูลผู้ใช้ (${currentCount}/${totalItems})`}));
                                        }
                                        // 2. ST5
                                        for(const s of data.st5) {
                                            const { id, ...rest } = s;
                                            await setDoc(doc(db, 'artifacts', appId, 'public', 'data', 'st5', id), rest);
                                            currentCount++;
                                            setRestoreStatus(prev => ({...prev, current: currentCount, message: `กำลังกู้คืนข้อมูล ST-5 (${currentCount}/${totalItems})`}));
                                        }
                                        // 3. Behaviors
                                        for(const b of data.behaviors) {
                                            const { id, ...rest } = b;
                                            await setDoc(doc(db, 'artifacts', appId, 'public', 'data', 'behaviors', id), rest);
                                            currentCount++;
                                            setRestoreStatus(prev => ({...prev, current: currentCount, message: `กำลังกู้คืนข้อมูลพฤติกรรม (${currentCount}/${totalItems})`}));
                                        }
                                        
                                        setRestoreStatus(prev => ({...prev, current: totalItems, message: 'กู้คืนข้อมูลเรียบร้อยแล้ว!', finished: true}));
                                    } catch(err) {
                                        setRestoreStatus(prev => ({...prev, message: 'เกิดข้อผิดพลาด: ' + err.message, error: err.message, finished: true}));
                                    }
                                }, 'danger');"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open('src/App.tsx', 'w') as f:
        f.write(content)
    print("Patch applied successfully.")
else:
    print("Could not find the target text to replace.")
