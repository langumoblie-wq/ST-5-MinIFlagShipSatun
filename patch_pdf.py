import sys

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "const handleExportPDF = async () => {" in line:
        start_idx = i
        break
for i in range(start_idx, len(lines)):
    if "const renderKPIs = () => (" in lines[i]:
        end_idx = i
        break

new_logic = """  // Export PDF Logic
  const handleExportPDF = async () => {
    if (!printRef.current) return;
    setIsExporting(true);
    try {
      const element = printRef.current;
      
      // Temporarily show the element to capture it
      const originalDisplay = element.style.display;
      element.style.display = 'block';
      element.style.position = 'absolute';
      element.style.top = '-9999px';
      
      // Wait for React to render and fonts to load
      await new Promise(resolve => setTimeout(resolve, 500));
      
      const canvas = await toPng(element, { 
          quality: 1.0, 
          backgroundColor: '#ffffff', 
          pixelRatio: 2,
          width: 794
      });
      
      // Hide it again
      element.style.display = originalDisplay;
      
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (element.offsetHeight * pdfWidth) / 794; 
      
      pdf.addImage(canvas, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`Executive_Report_${new Date().getTime()}.pdf`);
    } catch (err) {
      console.error(err);
      alert('เกิดข้อผิดพลาดในการสร้าง PDF');
    } finally {
      setIsExporting(false);
    }
  };

"""
lines[start_idx:end_idx] = [new_logic]

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.writelines(lines)
