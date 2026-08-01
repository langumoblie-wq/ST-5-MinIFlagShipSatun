import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

old_start = """function ImportDashboard({ triggerAlert, triggerConfirm, profile }) {
  const [inputText, setInputText] = useState('');
  const [parsedData, setParsedData] = useState([]);
  const [affiliation, setAffiliation] = useState(schoolOptions[0]);
  const [isImporting, setIsImporting] = useState(false);"""

new_start = """function ImportDashboard({ triggerAlert, triggerConfirm, profile }) {
  const [inputText, setInputText] = useState('');
  const [parsedData, setParsedData] = useState([]);
  const [affiliation, setAffiliation] = useState(schoolOptions[0]);
  const [isImporting, setIsImporting] = useState(false);
  const [duplicateCheck, setDuplicateCheck] = useState(null);
  const [importSummary, setImportSummary] = useState(null);"""

if old_start in content:
    content = content.replace(old_start, new_start)
else:
    print("Failed to replace old_start")

old_handleImport = """  const handleImport = async () => {
    if (parsedData.length === 0) return;
    triggerConfirm(`ยืนยันการนำเข้าข้อมูลนักเรียนจำนวน ${parsedData.length} รายการใช่หรือไม่?`, async () => {
      setIsImporting(true);
      try {
        const timestamp = Date.now();
        let successCount = 0;
        
        for (const student of parsedData) {
          const usernameKey = student.username.toLowerCase();
          
          // 1. Create User
          const userData = {
            username: usernameKey,
            password: student.password,
            name: student.name,
            accountType: 'student',
            role: 'student',
            affiliation: affiliation,
            status: 'approved',
            createdAt: timestamp
          };
          await setDoc(doc(db, 'artifacts', appId, 'public', 'data', 'users', usernameKey), userData);
          syncToGoogleSheet('REGISTER', { username: usernameKey, ...userData });
          
          // 2. Create ST-5 Record
          const st5Obj = calculateST5(student.score);
          const st5Data = {
            uid: usernameKey,
            userId: usernameKey,
            userName: student.name,
            answers: student.answers,
            score: student.score,
            level: st5Obj.level,
            timestamp: timestamp,
            suggestion: ''
          };
          await addDoc(collection(db, 'artifacts', appId, 'public', 'data', 'st5'), st5Data);
          syncToGoogleSheet('ST5', st5Data);
          
          successCount++;
        }
        
        triggerAlert(`นำเข้าข้อมูลสำเร็จ ${successCount} รายการ`, 'success');
        setInputText('');
        setParsedData([]);
      } catch (err) {
        console.error("Import error:", err);
        triggerAlert('เกิดข้อผิดพลาดในการนำเข้า: ' + err.message, 'error');
      } finally {
        setIsImporting(false);
      }
    });
  };"""

new_handleImport = """  const handleImport = async () => {
    if (parsedData.length === 0) return;
    triggerConfirm(`ยืนยันการนำเข้าข้อมูลนักเรียนจำนวน ${parsedData.length} รายการใช่หรือไม่?`, async () => {
      setIsImporting(true);
      try {
        const timestamp = Date.now();
        let successCount = 0;
        let overwriteCount = 0;
        let skipCount = 0;
        
        for (const student of parsedData) {
          const usernameKey = student.username.toLowerCase();
          
          const docRef = doc(db, 'artifacts', appId, 'public', 'data', 'users', usernameKey);
          const snap = await getDoc(docRef);
          
          let shouldImport = true;
          let isOverwrite = false;
          
          if (snap.exists()) {
             shouldImport = await new Promise((resolve) => {
                 setDuplicateCheck({ student, resolve });
             });
             setDuplicateCheck(null);
             if (shouldImport) isOverwrite = true;
          }
          
          if (!shouldImport) {
             skipCount++;
             continue;
          }
          
          // 1. Create User
          const userData = {
            username: usernameKey,
            password: student.password,
            name: student.name,
            accountType: 'student',
            role: 'student',
            affiliation: affiliation,
            status: 'approved',
            createdAt: timestamp
          };
          await setDoc(docRef, userData);
          syncToGoogleSheet('REGISTER', { username: usernameKey, ...userData });
          
          // 2. Create ST-5 Record
          const st5Obj = calculateST5(student.score);
          const st5Data = {
            uid: usernameKey,
            userId: usernameKey,
            userName: student.name,
            answers: student.answers,
            score: student.score,
            level: st5Obj.level,
            timestamp: timestamp,
            suggestion: ''
          };
          await addDoc(collection(db, 'artifacts', appId, 'public', 'data', 'st5'), st5Data);
          syncToGoogleSheet('ST5', st5Data);
          
          if (isOverwrite) overwriteCount++;
          else successCount++;
        }
        
        setImportSummary({
           total: parsedData.length,
           success: successCount,
           overwritten: overwriteCount,
           skipped: skipCount
        });
        
        setInputText('');
        setParsedData([]);
      } catch (err) {
        console.error("Import error:", err);
        triggerAlert('เกิดข้อผิดพลาดในการนำเข้า: ' + err.message, 'error');
      } finally {
        setIsImporting(false);
      }
    });
  };"""

if old_handleImport in content:
    content = content.replace(old_handleImport, new_handleImport)
else:
    print("Failed to replace handleImport")

old_return = """    <div className="bg-white p-6 md:p-10 rounded-[2.5rem] shadow-sm border border-slate-100 max-w-5xl mx-auto">"""
new_return = """    <>
    <div className="bg-white p-6 md:p-10 rounded-[2.5rem] shadow-sm border border-slate-100 max-w-5xl mx-auto">"""

if old_return in content:
    content = content.replace(old_return, new_return)
else:
    print("Failed to replace return start")

old_end = """      </div>
    </div>
  );
}"""

new_end = """      </div>
    </div>
    
    {/* Duplicate Confirmation Modal */}
    {duplicateCheck && (
        <div className="fixed inset-0 z-[200] flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-in fade-in">
           <div className="bg-white p-6 md:p-8 rounded-[2rem] max-w-md w-full shadow-2xl border border-slate-100 text-center space-y-5 animate-in zoom-in-95">
              <div className="mx-auto w-16 h-16 bg-amber-100 text-amber-600 rounded-full flex items-center justify-center shadow-inner border-2 border-white mb-2">
                 <AlertCircle size={32} />
              </div>
              <h3 className="text-xl font-black text-slate-800">พบข้อมูลซ้ำซ้อน</h3>
              <p className="text-slate-600 text-sm">
                 ผู้ใช้: <span className="font-bold text-slate-800">{duplicateCheck.student.name}</span><br />
                 (Username: <span className="font-mono bg-slate-100 px-2 py-0.5 rounded text-slate-700">{duplicateCheck.student.username}</span>)<br />
                 มีอยู่ในระบบอยู่แล้ว คุณต้องการนำเข้าข้อมูลใหม่ไปทับข้อมูลเดิมหรือไม่?
              </p>
              <div className="flex gap-3 pt-4">
                 <button 
                    onClick={() => duplicateCheck.resolve(false)}
                    className="flex-1 py-3 bg-slate-100 text-slate-600 font-bold rounded-xl hover:bg-slate-200 transition"
                 >
                    ยกเลิก (ข้ามรายการนี้)
                 </button>
                 <button 
                    onClick={() => duplicateCheck.resolve(true)}
                    className="flex-1 py-3 bg-amber-500 text-white font-bold rounded-xl hover:bg-amber-600 shadow-md transition"
                 >
                    ยืนยัน (เขียนทับ)
                 </button>
              </div>
           </div>
        </div>
    )}

    {/* Import Summary Modal */}
    {importSummary && (
        <div className="fixed inset-0 z-[200] flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-in fade-in">
           <div className="bg-white p-6 md:p-8 rounded-[2rem] max-w-md w-full shadow-2xl border border-slate-100 text-center space-y-5 animate-in zoom-in-95">
              <div className="mx-auto w-16 h-16 bg-teal-100 text-teal-600 rounded-full flex items-center justify-center shadow-inner border-2 border-white mb-2">
                 <CheckCircle2 size={32} />
              </div>
              <h3 className="text-xl font-black text-slate-800">สรุปผลการนำเข้าข้อมูล</h3>
              
              <div className="bg-slate-50 rounded-2xl p-4 space-y-3 text-left">
                  <div className="flex justify-between items-center text-sm">
                      <span className="text-slate-500 font-medium">รายการทั้งหมด</span>
                      <span className="font-bold text-slate-800">{importSummary.total}</span>
                  </div>
                  <div className="flex justify-between items-center text-sm border-t border-slate-200 pt-3">
                      <span className="text-teal-600 font-medium">นำเข้าใหม่สำเร็จ</span>
                      <span className="font-bold text-teal-600">{importSummary.success}</span>
                  </div>
                  <div className="flex justify-between items-center text-sm border-t border-slate-200 pt-3">
                      <span className="text-amber-600 font-medium">เขียนทับสำเร็จ</span>
                      <span className="font-bold text-amber-600">{importSummary.overwritten}</span>
                  </div>
                  <div className="flex justify-between items-center text-sm border-t border-slate-200 pt-3">
                      <span className="text-slate-500 font-medium">ข้ามรายการ</span>
                      <span className="font-bold text-slate-500">{importSummary.skipped}</span>
                  </div>
              </div>

              <div className="pt-2">
                 <button 
                    onClick={() => setImportSummary(null)}
                    className="w-full py-4 bg-slate-800 text-white font-bold rounded-xl hover:bg-slate-700 shadow-md transition"
                 >
                    ปิดหน้าต่าง
                 </button>
              </div>
           </div>
        </div>
    )}
    </>
  );
}"""

if old_end in content:
    content = content.replace(old_end, new_end)
else:
    print("Failed to replace return end")

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("Updated ImportDashboard with duplicate check and summary")

