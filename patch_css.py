import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

css_target = """      <style dangerouslySetInnerHTML={{__html: `
        .hide-scrollbar::-webkit-scrollbar { display: none; }
        .hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
        .custom-scrollbar::-webkit-scrollbar { width: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background-color: #cbd5e1; border-radius: 20px; }
      `}} />"""

css_replacement = """      <style dangerouslySetInnerHTML={{__html: `
        .hide-scrollbar::-webkit-scrollbar { display: none; }
        .hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
        .custom-scrollbar::-webkit-scrollbar { width: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background-color: #cbd5e1; border-radius: 20px; }
        
        @media print {
          /* ซ่อน sidebar และส่วนที่ไม่จำเป็น */
          body { background-color: white !important; }
          .md\\\\:w-64, .md\\\\:w-72, .lg\\\\:w-72 { display: none !important; }
          .no-print, .hide-on-print { display: none !important; }
          .print-only { display: block !important; }
          .flex-1 { padding: 0 !important; background: white !important; }
          
          /* ปรับแต่งสำหรับการพิมพ์ */
          .print-container { width: 100% !important; margin: 0 !important; padding: 20px !important; }
          .print-card { 
            border: 1px solid #e2e8f0 !important; 
            box-shadow: none !important; 
            break-inside: avoid; 
            margin-bottom: 20px;
            background: white !important;
          }
          * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
        }
      `}} />"""

if css_target in content:
    content = content.replace(css_target, css_replacement)
    print("CSS patched")
else:
    print("CSS NOT found")

with open('src/App.tsx', 'w') as f:
    f.write(content)
