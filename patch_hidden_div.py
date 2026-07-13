import re

with open('src/App.tsx', 'r') as f:
    code = f.read()

pattern = re.compile(r'(<style dangerouslySetInnerHTML={{__html: `\s*\.hide-scrollbar::-webkit-scrollbar \{ display: none; \}\s*\.hide-scrollbar \{ -ms-overflow-style: none; scrollbar-width: none; \}\s*`}} />\s*</div>\s*\);\s*\})')

match = pattern.search(code)
if match:
    new_end = """<style dangerouslySetInnerHTML={{__html: `
        .hide-scrollbar::-webkit-scrollbar { display: none; }
        .hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
      `}} />

      {/* Hidden Div for Generating Consent PDF via triggerDownloadConsentPdf */}
      {downloadPdfUser && (
        <div className="fixed top-[-9999px] left-[-9999px] w-[800px] bg-white text-black overflow-hidden pointer-events-none z-[-100]">
           <div id="consent-pdf-generic">
             <ConsentDocument 
                 name={downloadPdfUser.name} 
                 dateStr={downloadPdfUser.createdAt ? new Date(downloadPdfUser.createdAt).toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' }) : new Date().toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' })}
                 hidePrintBtn={true}
                 onPrint={() => {}}
             />
           </div>
        </div>
      )}
    </div>
  );
}"""
    code = code[:match.start()] + new_end + code[match.end():]
    with open('src/App.tsx', 'w') as f:
        f.write(code)
    print("Patched end of App")
else:
    print("Not found")

