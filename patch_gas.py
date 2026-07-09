import re

with open("src/App.tsx", "r") as f:
    content = f.read()

# Replace firestore mock imports with gasDb imports
content = re.sub(
    r"import \{ initAuth, googleSignIn, getAccessToken, logout as googleLogout \} from '\./lib/googleAuth';\nimport \{ initializeSheets \} from '\./lib/sheetsDb';",
    "",
    content
)

content = content.replace(
    "import { \n  getFirestore, doc, setDoc, getDoc, getDocs, onSnapshot, addDoc, updateDoc, deleteDoc, collection\n} from './lib/sheetsDbMock';",
    "import { getFirestore, doc, setDoc, getDoc, getDocs, onSnapshot, addDoc, updateDoc, deleteDoc, collection } from './lib/gasDb';"
)
content = content.replace(
    "import { \n  getFirestore, doc, setDoc, getDoc, getDocs, onSnapshot, addDoc, updateDoc, deleteDoc, collection\n} from 'firebase/firestore';",
    "import { getFirestore, doc, setDoc, getDoc, getDocs, onSnapshot, addDoc, updateDoc, deleteDoc, collection } from './lib/gasDb';"
)

content = content.replace("const db = getFirestore(app, firebaseConfig.firestoreDatabaseId);", "const db = getFirestore();")
content = content.replace("const db = getFirestore();", "const db = getFirestore();")

# We need to remove googleUser and googleToken logic
content = re.sub(r"const \[googleUser, setGoogleUser\] = useState\(null\);", "", content)
content = re.sub(r"const \[googleToken, setGoogleToken\] = useState\(null\);", "", content)

init_block = """  useEffect(() => {
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

new_init_block = """  useEffect(() => {
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

content = content.replace(init_block, new_init_block)

no_profile_block = """  if (!googleUser || !googleToken) {
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

  if (!profile) {"""

new_no_profile_block = """  if (!profile) {"""
content = content.replace(no_profile_block, new_no_profile_block)

logout_block = """  const handleLogout = () => {
    localStorage.removeItem(`${appId}_session`);
    setProfile(null);
    googleLogout();
    triggerAlert('ออกจากระบบเรียบร้อยแล้วค่ะ ไว้พบกันใหม่นะ', 'success');
  };"""
new_logout_block = """  const handleLogout = () => {
    localStorage.removeItem(`${appId}_session`);
    setProfile(null);
    triggerAlert('ออกจากระบบเรียบร้อยแล้วค่ะ ไว้พบกันใหม่นะ', 'success');
  };"""
content = content.replace(logout_block, new_logout_block)

# Clean up syncToGoogleSheet to just be a no-op since gasDb handles it
sync_block = """const syncToGoogleSheet = async (type, payload) => {
  if (!GOOGLE_WEBAPP_URL) return;
  try {
    await fetch(GOOGLE_WEBAPP_URL, {
      method: 'POST',
      mode: 'no-cors', 
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type, data: payload })
    });
  } catch (error) {
    console.error("Sheet Sync Error:", error);
  }
};"""

new_sync_block = """const syncToGoogleSheet = async (type: string, payload: any) => {
  // DB is now handled natively via gasDb.ts
};"""
content = content.replace(sync_block, new_sync_block)

with open("src/App.tsx", "w") as f:
    f.write(content)

print("Patch applied")
