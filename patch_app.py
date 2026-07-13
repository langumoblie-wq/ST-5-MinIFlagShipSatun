import re

with open('src/App.tsx', 'r') as f:
    code = f.read()

old_trigger_confirm = """  const triggerConfirm = (message, onConfirmCallback) => {
    setConfirmConfig({
      isOpen: true,
      message,
      onConfirm: () => {
        if (onConfirmCallback) onConfirmCallback();
        setConfirmConfig(prev => ({ ...prev, isOpen: false }));
      }
    });
  };"""

new_trigger_confirm = """  const triggerConfirm = (message, onConfirmCallback) => {
    setConfirmConfig({
      isOpen: true,
      message,
      onConfirm: () => {
        if (onConfirmCallback) onConfirmCallback();
        setConfirmConfig(prev => ({ ...prev, isOpen: false }));
      }
    });
  };

  const [downloadPdfUser, setDownloadPdfUser] = useState(null);

  const triggerDownloadConsentPdf = async (user) => {
    setDownloadPdfUser(user);
    setTimeout(async () => {
      const element = document.getElementById(`consent-pdf-generic`);
      if (!element) return;
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
        triggerAlert('กำลังสร้างไฟล์ PDF กรุณารอสักครู่...', 'info');
        const dataUrl = await toPng(element, { quality: 0.95, pixelRatio: 2, backgroundColor: '#ffffff' });
        const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
        const imgProps = pdf.getImageProperties(dataUrl);
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
        pdf.addImage(dataUrl, 'PNG', 0, 0, pdfWidth, pdfHeight);
        pdf.save(`ConsentForm_${user.name}.pdf`);
        triggerAlert('โหลด Consent Form สำเร็จ', 'success');
      } catch (err) {
        console.error(err);
        triggerAlert('เกิดข้อผิดพลาดในการสร้าง PDF', 'error');
      } finally {
        element.style.position = originalStyles.position;
        element.style.left = originalStyles.left;
        element.style.top = originalStyles.top;
        element.style.width = originalStyles.width;
        setDownloadPdfUser(null);
      }
    }, 500);
  };"""

code = code.replace(old_trigger_confirm, new_trigger_confirm)

# Pass it down to dashboards
old_dashboards = """            {activeTab === 'dashboard' && profile.role === 'user' && <UserDashboard users={usersList} profile={profile} st5Data={st5Data} behaviorData={behaviorData} triggerAlert={triggerAlert} triggerConfirm={triggerConfirm} />}
            {activeTab === 'dashboard' && profile.role === 'admin' && <AdminDashboard users={usersList} st5Data={st5Data} behaviorData={behaviorData} profile={profile} triggerAlert={triggerAlert} triggerConfirm={triggerConfirm} />}
            {activeTab === 'dashboard' && profile.role === 'superadmin' && <SuperAdminDashboard users={usersList} st5Data={st5Data} behaviorData={behaviorData} profile={profile} triggerAlert={triggerAlert} triggerConfirm={triggerConfirm} />}"""

new_dashboards = """            {activeTab === 'dashboard' && profile.role === 'user' && <UserDashboard users={usersList} profile={profile} st5Data={st5Data} behaviorData={behaviorData} triggerAlert={triggerAlert} triggerConfirm={triggerConfirm} />}
            {activeTab === 'dashboard' && profile.role === 'admin' && <AdminDashboard users={usersList} st5Data={st5Data} behaviorData={behaviorData} profile={profile} triggerAlert={triggerAlert} triggerConfirm={triggerConfirm} triggerDownloadConsentPdf={triggerDownloadConsentPdf} />}
            {activeTab === 'dashboard' && profile.role === 'superadmin' && <SuperAdminDashboard users={usersList} st5Data={st5Data} behaviorData={behaviorData} profile={profile} triggerAlert={triggerAlert} triggerConfirm={triggerConfirm} triggerDownloadConsentPdf={triggerDownloadConsentPdf} />}"""

code = code.replace(old_dashboards, new_dashboards)

# Render hidden pdf div
old_app_end = """      {/* Global Confirm Modal */}
      <CustomConfirmModal 
        isOpen={confirmConfig.isOpen}
        message={confirmConfig.message}
        onConfirm={confirmConfig.onConfirm}
        onCancel={() => setConfirmConfig(prev => ({ ...prev, isOpen: false }))}
      />
    </div>
  );
}"""

new_app_end = """      {/* Global Confirm Modal */}
      <CustomConfirmModal 
        isOpen={confirmConfig.isOpen}
        message={confirmConfig.message}
        onConfirm={confirmConfig.onConfirm}
        onCancel={() => setConfirmConfig(prev => ({ ...prev, isOpen: false }))}
      />

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

code = code.replace(old_app_end, new_app_end)

with open('src/App.tsx', 'w') as f:
    f.write(code)
print("Patched App.tsx!")
