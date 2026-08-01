import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

old_header = """      <div className="flex items-center gap-4 mb-8 pb-6 border-b border-slate-100">
        <div className="w-14 h-14 bg-teal-100 rounded-2xl flex items-center justify-center text-teal-600 shadow-inner border-2 border-white">
          <Database size={28} strokeWidth={2.5} />
        </div>
        <div>
          <h2 className="text-2xl font-black text-slate-800">นำเข้าข้อมูล (Import)</h2>
          <p className="text-slate-500 font-medium">นำเข้าข้อมูลผู้ใช้งาน และประวัติคัดกรอง ST-5 จากตาราง PDF หรือ Excel</p>
        </div>
      </div>"""

new_header = """      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8 pb-6 border-b border-slate-100">
        <div className="flex items-center gap-4">
            <div className="w-14 h-14 bg-teal-100 rounded-2xl flex items-center justify-center text-teal-600 shadow-inner border-2 border-white shrink-0">
            <Database size={28} strokeWidth={2.5} />
            </div>
            <div>
            <h2 className="text-2xl font-black text-slate-800">จัดการข้อมูล (Import / Backup)</h2>
            <p className="text-slate-500 font-medium">นำเข้าข้อมูลจากตาราง PDF หรือ Excel และสำรอง/กู้คืนข้อมูลทั้งระบบ (JSON)</p>
            </div>
        </div>
        <div className="flex items-center gap-2">
            <button 
                onClick={async () => {
                   triggerConfirm('ยืนยันการสำรองข้อมูลทั้งหมดในระบบ (Users, ST-5, Behaviors) ออกเป็นไฟล์ JSON?', async () => {
                       try {
                           const usersSnap = await getDocs(collection(db, 'artifacts', appId, 'public', 'data', 'users'));
                           const st5Snap = await getDocs(collection(db, 'artifacts', appId, 'public', 'data', 'st5'));
                           const behSnap = await getDocs(collection(db, 'artifacts', appId, 'public', 'data', 'behaviors'));
                           
                           const data = {
                               users: usersSnap.docs.map(d => ({ id: d.id, ...d.data() })),
                               st5: st5Snap.docs.map(d => ({ id: d.id, ...d.data() })),
                               behaviors: behSnap.docs.map(d => ({ id: d.id, ...d.data() })),
                               timestamp: new Date().toISOString()
                           };
                           
                           const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                           const url = URL.createObjectURL(blob);
                           const a = document.createElement('a');
                           a.href = url;
                           a.download = `st5_backup_${new Date().toISOString().split('T')[0]}.json`;
                           document.body.appendChild(a);
                           a.click();
                           document.body.removeChild(a);
                           URL.revokeObjectURL(url);
                           triggerAlert('ดาวน์โหลดไฟล์สำรองข้อมูลเรียบร้อยแล้ว', 'success');
                       } catch(err) {
                           triggerAlert('เกิดข้อผิดพลาดในการสำรองข้อมูล: ' + err.message, 'error');
                       }
                   });
                }}
                className="px-4 py-2 bg-indigo-50 text-indigo-600 border border-indigo-200 hover:bg-indigo-100 font-bold rounded-xl flex items-center gap-2 transition"
            >
                <Download size={18} /> สำรองข้อมูล (Backup)
            </button>
            <label className="px-4 py-2 bg-slate-800 text-white border border-slate-700 hover:bg-slate-700 font-bold rounded-xl flex items-center gap-2 transition cursor-pointer">
                <Database size={18} /> กู้คืนข้อมูล (Restore)
                <input 
                    type="file" 
                    accept=".json" 
                    className="hidden" 
                    onChange={(e) => {
                        const file = e.target.files[0];
                        if(!file) return;
                        
                        const reader = new FileReader();
                        reader.onload = (evt) => {
                            try {
                                const data = JSON.parse(evt.target.result);
                                if(!data.users || !data.st5 || !data.behaviors) {
                                    triggerAlert('ไฟล์สำรองข้อมูลไม่ถูกต้อง หรือไม่สมบูรณ์', 'error');
                                    return;
                                }
                                
                                triggerConfirm(`คำเตือน: การกู้คืนข้อมูลจะนำข้อมูลจากไฟล์ (Users: ${data.users.length}, ST-5: ${data.st5.length}, Behaviors: ${data.behaviors.length}) เพิ่ม/ทับลงในระบบ ยืนยันหรือไม่?`, async () => {
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
                                }, 'danger');
                            } catch(err) {
                                triggerAlert('ไม่สามารถอ่านไฟล์ JSON ได้', 'error');
                            }
                        };
                        reader.readAsText(file);
                        e.target.value = ''; // reset
                    }}
                />
            </label>
        </div>
      </div>"""

if old_header in content:
    content = content.replace(old_header, new_header)
else:
    print("Could not find old_header")

with open('src/App.tsx', 'w') as f:
    f.write(content)
