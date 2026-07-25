import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

target = """  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="space-y-6 print-container animate-in fade-in duration-500 bg-slate-50/50 min-h-screen p-2 md:p-4 rounded-3xl">
      
      <div className="bg-white p-6 md:p-8 rounded-[2rem] shadow-sm border border-slate-100 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div className="flex gap-4 items-start">
           <div className="text-blue-600 mt-1">
             <Trophy size={32} strokeWidth={2} />
           </div>
           <div>
             <h2 className="text-xl md:text-2xl font-black text-slate-800">สรุปผลและการติดตามโครงการ</h2>
             <p className="text-xs md:text-sm text-slate-500 font-medium mt-1">ติดตามความก้าวหน้าการคัดกรองแยกตามโมเดลและพื้นที่เป้าหมาย</p>
           </div>
        </div>

        <div className="flex flex-col md:flex-row items-stretch md:items-center gap-4 w-full md:w-auto">
          <button onClick={handlePrint} className="bg-slate-50 hover:bg-slate-100 text-slate-700 border border-slate-200 px-4 py-2.5 rounded-xl font-bold flex items-center justify-center gap-2 transition shadow-sm text-sm no-print">
            <Printer size={16} /> พิมพ์รายงาน
          </button>"""

replacement = """  const [isPrinting, setIsPrinting] = useState(false);

  const handlePrint = async () => {
    setIsPrinting(true);
    setTimeout(async () => {
        const element = document.getElementById('report-dashboard-container');
        if (!element) {
            setIsPrinting(false);
            return;
        }
        try {
            const dataUrl = await toPng(element, { 
                quality: 0.95, 
                pixelRatio: 2, 
                backgroundColor: '#f8fafc',
                filter: (node) => {
                    if (node.classList && node.classList.contains('no-print')) {
                        return false;
                    }
                    return True;
                }
            });
            const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
            const imgProps = pdf.getImageProperties(dataUrl);
            const pdfWidth = pdf.internal.pageSize.getWidth();
            const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
            
            let position = 0;
            let heightLeft = pdfHeight;
            const pageHeight = pdf.internal.pageSize.getHeight();
            
            pdf.addImage(dataUrl, 'PNG', 0, position, pdfWidth, pdfHeight);
            heightLeft -= pageHeight;
            
            while (heightLeft > 0) {
                position = heightLeft - pdfHeight;
                pdf.addPage();
                pdf.addImage(dataUrl, 'PNG', 0, position, pdfWidth, pdfHeight);
                heightLeft -= pageHeight;
            }
            
            pdf.save(`project_report_${new Date().getTime()}.pdf`);
        } catch (err) {
            console.error('Error generating PDF', err);
        } finally {
            setIsPrinting(false);
        }
    }, 100);
  };

  return (
    <div id="report-dashboard-container" className="space-y-6 print-container animate-in fade-in duration-500 bg-slate-50/50 min-h-screen p-2 md:p-4 rounded-3xl">
      
      <div className="bg-white p-6 md:p-8 rounded-[2rem] shadow-sm border border-slate-100 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div className="flex gap-4 items-start">
           <div className="text-blue-600 mt-1">
             <Trophy size={32} strokeWidth={2} />
           </div>
           <div>
             <h2 className="text-xl md:text-2xl font-black text-slate-800">สรุปผลและการติดตามโครงการ</h2>
             <p className="text-xs md:text-sm text-slate-500 font-medium mt-1">ติดตามความก้าวหน้าการคัดกรองแยกตามโมเดลและพื้นที่เป้าหมาย</p>
           </div>
        </div>

        <div className="flex flex-col md:flex-row items-stretch md:items-center gap-4 w-full md:w-auto">
          <button onClick={handlePrint} disabled={isPrinting} className={`bg-slate-50 hover:bg-slate-100 text-slate-700 border border-slate-200 px-4 py-2.5 rounded-xl font-bold flex items-center justify-center gap-2 transition shadow-sm text-sm no-print ${isPrinting ? 'opacity-50 cursor-not-allowed' : ''}`}>
            {isPrinting ? <RefreshCw size={16} className="animate-spin" /> : <Printer size={16} />} 
            {isPrinting ? 'กำลังเตรียม PDF...' : 'พิมพ์รายงาน'}
          </button>"""

if target in content:
    content = content.replace(target, replacement)
    with open('src/App.tsx', 'w') as f:
        f.write(content)
    print("Replaced successfully")
else:
    print("Target not found")
