import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update handleExportPDF
old_export = """      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (element.offsetHeight * pdfWidth) / 794; 
      
      let position = 0;
      let heightLeft = pdfHeight;
      const pageHeight = pdf.internal.pageSize.getHeight();
      
      pdf.addImage(canvas, 'PNG', 0, position, pdfWidth, pdfHeight);
      heightLeft -= pageHeight;
      
      while (heightLeft > 0) {
          position = heightLeft - pdfHeight;
          pdf.addPage();
          pdf.addImage(canvas, 'PNG', 0, position, pdfWidth, pdfHeight);
          heightLeft -= pageHeight;
      }
      
      pdf.save(`Executive_Report_${new Date().getTime()}.pdf`);"""

new_export = """      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();

      const pages = Array.from(element.children);
      
      for (let i = 0; i < pages.length; i++) {
        const pageEl = pages[i];
        const pageCanvas = await toPng(pageEl, { 
          quality: 1.0, 
          backgroundColor: '#ffffff', 
          pixelRatio: 2, 
          width: 794 
        });
        
        const pageImgHeight = (pageEl.offsetHeight * pdfWidth) / 794;
        
        if (i > 0) pdf.addPage();
        
        // If content is longer than A4, scale it down to fit one page.
        // Otherwise, draw it at natural size.
        const finalHeight = pageImgHeight > pageHeight ? pageHeight : pageImgHeight;
        
        pdf.addImage(pageCanvas, 'PNG', 0, 0, pdfWidth, finalHeight);
      }
      
      pdf.save(`Executive_Report_${new Date().getTime()}.pdf`);"""

if old_export in content:
    content = content.replace(old_export, new_export)
    print("Replaced handleExportPDF logic")
else:
    print("Could not find handleExportPDF logic")

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
