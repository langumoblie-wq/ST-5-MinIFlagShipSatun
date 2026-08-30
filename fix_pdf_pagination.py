import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_pdf_logic = """      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (element.offsetHeight * pdfWidth) / 794; 
      
      pdf.addImage(canvas, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`Executive_Report_${new Date().getTime()}.pdf`);"""

new_pdf_logic = """      const pdf = new jsPDF('p', 'mm', 'a4');
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

content = content.replace(old_pdf_logic, new_pdf_logic)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
