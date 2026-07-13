with open('src/App.tsx', 'r') as f:
    code = f.read()

old_buttons = """        <button onClick={() => {
             if (st5History.length === 0) {
               triggerAlert('ไม่สามารถประเมินพฤติกรรมได้ เนื่องจากยังไม่มีข้อมูลการประเมินสุขภาพจิต (ST-5)', 'error');
               return;
            }
            if (showBehaviorForm && !editingBehavior) {
               setShowBehaviorForm(false);
            } else {
               setEditingBehavior(null);
               setShowBehaviorForm(true);
               setViewingBehaviorResult(null);
            }
          }} 
           className="bg-slate-800 text-white px-6 py-4 rounded-2xl font-bold hover:bg-slate-700 shadow-md transition w-full md:w-auto text-sm"
        >
          {showBehaviorForm && !editingBehavior ? 'ปิดฟอร์มประเมิน' : '+ ประเมินพฤติกรรม'}
        </button>"""

new_buttons = """        <div className="flex flex-col md:flex-row gap-2 w-full md:w-auto">
          <button onClick={() => triggerDownloadConsentPdf(student)} className="bg-purple-100 text-purple-700 px-6 py-4 rounded-2xl font-bold hover:bg-purple-200 shadow-sm transition w-full md:w-auto text-sm flex items-center justify-center gap-2">
            <Download size={18} /> โหลด Consent Form
          </button>
          <button onClick={() => {
               if (st5History.length === 0) {
                 triggerAlert('ไม่สามารถประเมินพฤติกรรมได้ เนื่องจากยังไม่มีข้อมูลการประเมินสุขภาพจิต (ST-5)', 'error');
                 return;
              }
              if (showBehaviorForm && !editingBehavior) {
                 setShowBehaviorForm(false);
              } else {
                 setEditingBehavior(null);
                 setShowBehaviorForm(true);
                 setViewingBehaviorResult(null);
              }
            }} 
             className="bg-slate-800 text-white px-6 py-4 rounded-2xl font-bold hover:bg-slate-700 shadow-md transition w-full md:w-auto text-sm"
          >
            {showBehaviorForm && !editingBehavior ? 'ปิดฟอร์มประเมิน' : '+ ประเมินพฤติกรรม'}
          </button>
        </div>"""

if old_buttons in code:
    code = code.replace(old_buttons, new_buttons)
    with open('src/App.tsx', 'w') as f:
        f.write(code)
    print("Replaced old_buttons in AdminStudentDetail")
else:
    print("Could not find old_buttons in AdminStudentDetail. Trying regex.")
    import re
    # Using regex to find the button
    button_pattern = re.compile(r'<button onClick=\{\(\) => \{\s*if \(st5History\.length === 0\) \{[\s\S]*?\+ ประเมินพฤติกรรม\'\}\s*</button>')
    match = button_pattern.search(code)
    if match:
        code = code[:match.start()] + new_buttons + code[match.end():]
        with open('src/App.tsx', 'w') as f:
            f.write(code)
        print("Replaced old_buttons using regex")
    else:
        print("Still not found")
