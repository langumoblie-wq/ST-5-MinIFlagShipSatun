import re

with open("src/App.tsx", "r") as f:
    content = f.read()

# 1. Update imports
content = content.replace(
    "import React, { useState, useEffect, useMemo } from 'react';",
    "import React, { useState, useEffect, useMemo } from 'react';\nimport { initAuth, googleSignIn, getAccessToken, logout as googleLogout } from './lib/googleAuth';\nimport { initializeSheets } from './lib/sheetsDb';"
)

# 2. Add google session state
content = content.replace(
    "const [profile, setProfile] = useState(null);",
    "const [profile, setProfile] = useState(null);\n  const [googleUser, setGoogleUser] = useState(null);\n  const [googleToken, setGoogleToken] = useState(null);"
)

# 3. Modify initApp effect
old_init = """  useEffect(() => {
    const initApp = async () => {
      try {
        const savedSession = localStorage.getItem(`${appId}_session`);
        if (savedSession) {
          const docRef = doc(db, 'artifacts', appId, 'public', 'data', 'users', savedSession);
          const snap = await getDoc(docRef);
          if (snap.exists()) {
            setProfile({ id: snap.id, ...snap.data() });
          } else {
            localStorage.removeItem(`${appId}_session`);
          }
        }
      } catch (error) {
        console.error("Init error:", error);
      } finally {
        setLoading(false);
      }
    };
    initApp();
  }, []);"""

new_init = """  useEffect(() => {
    const unsubscribe = initAuth(
      async (user, token) => {
        setGoogleUser(user);
        setGoogleToken(token);
        
        // Now we can initialize the app and sheets
        try {
          await initializeSheets();
          const savedSession = localStorage.getItem(`${appId}_session`);
          if (savedSession) {
            const docRef = doc(db, 'artifacts', appId, 'public', 'data', 'users', savedSession);
            const snap = await getDoc(docRef);
            if (snap.exists()) {
              setProfile({ id: snap.id, ...snap.data() });
            } else {
              localStorage.removeItem(`${appId}_session`);
            }
          }
        } catch (error) {
          console.error("Init error:", error);
        } finally {
          setLoading(false);
        }
      },
      () => {
        setGoogleUser(null);
        setGoogleToken(null);
        setProfile(null);
        setLoading(false);
      }
    );
    return () => unsubscribe();
  }, []);"""

content = content.replace(old_init, new_init)

# 4. Modify handleLogout
old_logout = """  const handleLogout = () => {
    localStorage.removeItem(`${appId}_session`);
    setProfile(null);
    triggerAlert('ออกจากระบบเรียบร้อยแล้วค่ะ ไว้พบกันใหม่นะ', 'success');
  };"""

new_logout = """  const handleLogout = () => {
    localStorage.removeItem(`${appId}_session`);
    setProfile(null);
    googleLogout();
    triggerAlert('ออกจากระบบเรียบร้อยแล้วค่ะ ไว้พบกันใหม่นะ', 'success');
  };"""

content = content.replace(old_logout, new_logout)

# 5. Modify App return for !profile
old_no_profile = """  if (!profile) {
    return (
      <div style={{fontFamily: "'Kanit', sans-serif"}}>
        <AuthContainer onLogin={handleLogin} triggerAlert={triggerAlert} />
        <CuteAlert isOpen={alertConfig.isOpen} message={alertConfig.message} type={alertConfig.type} onClose={() => setAlertConfig({ ...alertConfig, isOpen: false })} />
      </div>
    );
  }"""

new_no_profile = """  if (!googleUser || !googleToken) {
    return (
      <div style={{fontFamily: "'Kanit', sans-serif"}} className="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-sky-50 flex flex-col items-center justify-center p-4">
        <div className="bg-white/90 p-8 rounded-[3rem] shadow-2xl shadow-purple-200/40 text-center max-w-md w-full">
          <HeartPulse className="text-purple-400 mx-auto mb-4" size={48} strokeWidth={2} />
          <h1 className="text-2xl font-extrabold text-slate-800 mb-2">เชื่อมต่อฐานข้อมูล</h1>
          <p className="text-slate-500 text-sm mb-8">โปรดเข้าสู่ระบบด้วยบัญชี Google เพื่อเข้าถึงข้อมูลแบบประเมินและรายชื่อนักเรียนผ่าน Google Sheets</p>
          <button 
            onClick={async () => {
              setLoading(true);
              try { await googleSignIn(); } 
              catch (err) { triggerAlert('การเข้าสู่ระบบ Google ล้มเหลว', 'error'); setLoading(false); }
            }}
            className="w-full bg-slate-800 text-white p-4 rounded-3xl font-bold hover:bg-slate-700 transition shadow-lg flex items-center justify-center gap-2"
          >
            <Database size={20} /> ลงชื่อเข้าใช้ด้วย Google
          </button>
        </div>
        <CuteAlert isOpen={alertConfig.isOpen} message={alertConfig.message} type={alertConfig.type} onClose={() => setAlertConfig({ ...alertConfig, isOpen: false })} />
      </div>
    );
  }

  if (!profile) {
    return (
      <div style={{fontFamily: "'Kanit', sans-serif"}}>
        <AuthContainer onLogin={handleLogin} triggerAlert={triggerAlert} />
        <CuteAlert isOpen={alertConfig.isOpen} message={alertConfig.message} type={alertConfig.type} onClose={() => setAlertConfig({ ...alertConfig, isOpen: false })} />
      </div>
    );
  }"""

content = content.replace(old_no_profile, new_no_profile)

with open("src/App.tsx", "w") as f:
    f.write(content)

print("Patch applied")
