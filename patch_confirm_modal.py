import re

with open('src/App.tsx', 'r') as f:
    code = f.read()

# 1. Update setConfirmConfig default
old_state = "const [confirmConfig, setConfirmConfig] = useState({ isOpen: false, message: '', onConfirm: null });"
new_state = "const [confirmConfig, setConfirmConfig] = useState({ isOpen: false, message: '', type: 'info', onConfirm: null });"
code = code.replace(old_state, new_state)

# 2. Update triggerConfirm
old_trigger = """  const triggerConfirm = (message, onConfirmCallback) => {
    setConfirmConfig({
      isOpen: true,
      message,
      onConfirm: () => {
        setConfirmConfig({ ...confirmConfig, isOpen: false });
        if (onConfirmCallback) onConfirmCallback();
      }
    });
  };"""

new_trigger = """  const triggerConfirm = (message, onConfirmCallback, type = 'info') => {
    setConfirmConfig({
      isOpen: true,
      message,
      type,
      onConfirm: () => {
        setConfirmConfig({ ...confirmConfig, isOpen: false });
        if (onConfirmCallback) onConfirmCallback();
      }
    });
  };"""

if old_trigger in code:
    code = code.replace(old_trigger, new_trigger)
else:
    print("Could not find old_trigger")

# 3. Update ConfirmModal rendering in App
old_modal_render = """<ConfirmModal isOpen={confirmConfig.isOpen} message={confirmConfig.message} onConfirm={confirmConfig.onConfirm} onCancel={() => setConfirmConfig({ ...confirmConfig, isOpen: false })} />"""
new_modal_render = """<ConfirmModal isOpen={confirmConfig.isOpen} message={confirmConfig.message} type={confirmConfig.type} onConfirm={confirmConfig.onConfirm} onCancel={() => setConfirmConfig({ ...confirmConfig, isOpen: false })} />"""
if old_modal_render in code:
    code = code.replace(old_modal_render, new_modal_render)
else:
    print("Could not find old_modal_render")

# 4. Update ConfirmModal function
old_modal_func = """function ConfirmModal({ isOpen, message, onConfirm, onCancel }) {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="w-full max-w-sm bg-white p-6 md:p-8 rounded-[2.5rem] shadow-2xl border border-slate-100 text-center space-y-5 animate-in zoom-in-95 duration-300">
        <div className="mx-auto w-20 h-20 rounded-full flex items-center justify-center shadow-lg transform scale-105 bg-indigo-50 text-indigo-500 border-2 border-indigo-100">
          <HelpCircle size={40} className="animate-pulse" />
        </div>
        <div>
          <h4 className="text-xl font-black text-slate-800">ยืนยันการดำเนินการ</h4>
          <p className="text-sm font-medium text-slate-500 leading-relaxed mt-2 whitespace-pre-line">{message}</p>
        </div>
        <div className="flex gap-3">
          <button 
            onClick={onCancel}
            className="flex-1 py-3.5 bg-slate-100 text-slate-500 rounded-3xl font-bold hover:bg-slate-200 transition text-sm"
          >
            ยกเลิก
          </button>
          <button 
            onClick={onConfirm}
            className="flex-1 py-3.5 bg-indigo-500 text-white rounded-3xl font-bold hover:bg-indigo-600 transition shadow-lg shadow-indigo-100 text-sm"
          >
            ยืนยัน
          </button>
        </div>
      </div>
    </div>
  );
}"""

new_modal_func = """function ConfirmModal({ isOpen, message, type = 'info', onConfirm, onCancel }) {
  if (!isOpen) return null;
  const isDanger = type === 'danger';
  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="w-full max-w-sm bg-white p-6 md:p-8 rounded-[2.5rem] shadow-2xl border border-slate-100 text-center space-y-5 animate-in zoom-in-95 duration-300">
        <div className={`mx-auto w-20 h-20 rounded-full flex items-center justify-center shadow-lg transform scale-105 ${isDanger ? 'bg-rose-50 text-rose-500 border-2 border-rose-100' : 'bg-indigo-50 text-indigo-500 border-2 border-indigo-100'}`}>
          {isDanger ? <AlertCircle size={40} className="animate-pulse" /> : <HelpCircle size={40} className="animate-pulse" />}
        </div>
        <div>
          <h4 className={`text-xl font-black ${isDanger ? 'text-rose-600' : 'text-slate-800'}`}>ยืนยันการดำเนินการ</h4>
          <p className="text-sm font-medium text-slate-500 leading-relaxed mt-2 whitespace-pre-line">{message}</p>
        </div>
        <div className="flex gap-3">
          <button 
            onClick={onCancel}
            className="flex-1 py-3.5 bg-slate-100 text-slate-500 rounded-3xl font-bold hover:bg-slate-200 transition text-sm"
          >
            ยกเลิก
          </button>
          <button 
            onClick={onConfirm}
            className={`flex-1 py-3.5 text-white rounded-3xl font-bold transition shadow-lg text-sm ${isDanger ? 'bg-rose-500 hover:bg-rose-600 shadow-rose-100' : 'bg-indigo-500 hover:bg-indigo-600 shadow-indigo-100'}`}
          >
            ยืนยัน
          </button>
        </div>
      </div>
    </div>
  );
}"""

if old_modal_func in code:
    code = code.replace(old_modal_func, new_modal_func)
else:
    print("Could not find old_modal_func")

with open('src/App.tsx', 'w') as f:
    f.write(code)
print("Updated ConfirmModal and triggerConfirm")
