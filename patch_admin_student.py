import re

with open('src/App.tsx', 'r') as f:
    code = f.read()

old_func_start = """function AdminStudentDetail({ student, st5History, behaviorHistory, onBack, triggerAlert, triggerConfirm }) {
  const [showBehaviorForm, setShowBehaviorForm] = useState(false);"""

new_func_start = """function AdminStudentDetail({ student, st5History, behaviorHistory, onBack, triggerAlert, triggerConfirm }) {
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

code = code.replace(old_func_start, new_func_start)

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
          <button onClick={downloadConsentPdf} disabled={isDownloadingPdf} className="bg-purple-100 text-purple-700 px-6 py-4 rounded-2xl font-bold hover:bg-purple-200 shadow-sm transition w-full md:w-auto text-sm flex items-center justify-center gap-2">
            <Download size={18} /> {isDownloadingPdf ? 'กำลังโหลด...' : 'โหลด Consent Form'}
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

code = code.replace(old_buttons, new_buttons)

old_html_end = """    <div className="max-w-6xl mx-auto space-y-6">"""

new_html_end = """    <div className="max-w-6xl mx-auto space-y-6">
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

code = code.replace(old_html_end, new_html_end)

with open('src/App.tsx', 'w') as f:
    f.write(code)
print("Patched AdminStudentDetail")
