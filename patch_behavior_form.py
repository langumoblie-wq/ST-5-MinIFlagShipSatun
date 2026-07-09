import re

with open("src/App.tsx", "r") as f:
    content = f.read()

# 1. Update BehaviorForm definition and handleSave
old_def = """function BehaviorForm({ targetUser, onDone, initialData }) {
  const [selections, setSelections] = useState(
    initialData ? initialData.selections : { desirable: [], undesirable: [] }
  );

  const toggleSelection = (type, item) => {
    setSelections(prev => {
      const current = prev[type];
      return current.includes(item) 
        ? { ...prev, [type]: current.filter(i => i !== item) }
        : { ...prev, [type]: [...current, item] };
    });
  };

  const handleSave = async () => {
    const timestamp = initialData ? initialData.timestamp : Date.now();
    const payload = { targetUid: targetUser.id, targetName: targetUser.name, selections, timestamp };
    
    if (initialData && initialData.id) {
      // โหมดแก้ไข
      await updateDoc(doc(db, 'artifacts', appId, 'public', 'data', 'behaviors', initialData.id), { selections });
      syncToGoogleSheet('EDIT_BEHAVIOR', payload);
    } else {
      // โหมดสร้างใหม่
      await addDoc(collection(db, 'artifacts', appId, 'public', 'data', 'behaviors'), payload);
      syncToGoogleSheet('BEHAVIOR', payload);
    }
    
    onDone();
  };"""

new_def = """function BehaviorForm({ targetUser, onDone, initialData, st5History }) {
  const [selections, setSelections] = useState(
    initialData ? initialData.selections : { desirable: [], undesirable: [], st5ReferenceId: '' }
  );

  const toggleSelection = (type, item) => {
    setSelections(prev => {
      const current = prev[type] || [];
      return current.includes(item) 
        ? { ...prev, [type]: current.filter(i => i !== item) }
        : { ...prev, [type]: [...current, item] };
    });
  };

  const handleSave = async () => {
    let finalTimestamp = Date.now();
    
    if (initialData) {
      finalTimestamp = initialData.timestamp;
    } else if (selections.st5ReferenceId && st5History) {
      const matchedSt5 = st5History.find(s => s.id === selections.st5ReferenceId);
      if (matchedSt5) {
        finalTimestamp = matchedSt5.timestamp;
      }
    }

    const payload = { targetUid: targetUser.id, targetName: targetUser.name, selections, timestamp: finalTimestamp };
    
    if (initialData && initialData.id) {
      // โหมดแก้ไข
      await updateDoc(doc(db, 'artifacts', appId, 'public', 'data', 'behaviors', initialData.id), { selections });
      syncToGoogleSheet('EDIT_BEHAVIOR', payload);
    } else {
      // โหมดสร้างใหม่
      await addDoc(collection(db, 'artifacts', appId, 'public', 'data', 'behaviors'), payload);
      syncToGoogleSheet('BEHAVIOR', payload);
    }
    
    onDone();
  };"""

content = content.replace(old_def, new_def)

# 2. Update BehaviorForm return UI
old_ui = """  return (
    <div className="bg-white p-6 md:p-8 rounded-[2.5rem] shadow-xl shadow-slate-200/40 border border-slate-100 mt-6 animate-in fade-in slide-in-from-top-4 duration-300">
      <div className="mb-8">
        <h3 className="text-2xl font-black text-slate-800">
          {initialData ? '✏️ แก้ไขแบบประเมินพฤติกรรม' : 'แบบประเมินพฤติกรรม'}
        </h3>
        <p className="text-slate-500 text-sm mt-1">เลือกติ๊กพฤติกรรมที่สังเกตเห็นในตัวนักเรียน</p>
      </div>"""

new_ui = """  return (
    <div className="bg-white p-6 md:p-8 rounded-[2.5rem] shadow-xl shadow-slate-200/40 border border-slate-100 mt-6 animate-in fade-in slide-in-from-top-4 duration-300">
      <div className="mb-8">
        <h3 className="text-xl font-black text-slate-800 flex items-center gap-2">
          <Star className="text-amber-400" size={24}/> {initialData ? 'แก้ไขการประเมินพฤติกรรม' : 'ประเมินพฤติกรรมนักเรียน'}
        </h3>
        <p className="text-sm text-slate-500 mt-2 font-medium">ทำเครื่องหมายพฤติกรรมที่พบ เพื่อจัดทำแผนพัฒนารายบุคคล</p>
      </div>

      {!initialData && st5History && st5History.length > 0 && (
        <div className="mb-6 p-5 bg-sky-50 rounded-[2rem] border border-sky-100">
          <label className="block text-sm font-bold text-sky-700 mb-2">อ้างอิงกับการประเมิน ST-5 ครั้งที่:</label>
          <select 
            className="w-full p-3.5 border border-sky-200 rounded-2xl bg-white outline-none focus:ring-4 focus:ring-sky-500/20 focus:border-sky-400 text-sm font-medium text-slate-700"
            value={selections.st5ReferenceId || ''}
            onChange={(e) => setSelections(prev => ({ ...prev, st5ReferenceId: e.target.value }))}
          >
            <option value="">-- ไม่ระบุ (ประเมินอิสระ) --</option>
            {st5History.map((item, idx) => (
              <option key={item.id} value={item.id}>
                ครั้งที่ {st5History.length - idx} ({new Date(item.timestamp).toLocaleDateString('th-TH')})
              </option>
            ))}
          </select>
        </div>
      )}"""

content = content.replace(old_ui, new_ui)

# 3. Update BehaviorForm usage in AdminStudentDetail
old_usage = """      {showBehaviorForm && (
        <BehaviorForm 
          targetUser={student} 
          initialData={editingBehavior}
          onDone={() => { 
            setShowBehaviorForm(false); 
            setEditingBehavior(null);
            triggerAlert(editingBehavior ? 'อัปเดตผลการประเมินพฤติกรรมเรียบร้อย' : 'บันทึกผลการประเมินพฤติกรรมลงระบบเรียบร้อย', 'success'); 
          }} 
        />
      )}"""

new_usage = """      {showBehaviorForm && (
        <BehaviorForm 
          targetUser={student} 
          initialData={editingBehavior}
          st5History={st5History}
          onDone={() => { 
            setShowBehaviorForm(false); 
            setEditingBehavior(null);
            triggerAlert(editingBehavior ? 'อัปเดตผลการประเมินพฤติกรรมเรียบร้อย' : 'บันทึกผลการประเมินพฤติกรรมลงระบบเรียบร้อย', 'success'); 
          }} 
        />
      )}"""

content = content.replace(old_usage, new_usage)

with open("src/App.tsx", "w") as f:
    f.write(content)

print("Patch applied")
