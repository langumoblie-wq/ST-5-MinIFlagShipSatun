import React, { useState, useEffect, useMemo, useRef } from 'react';
import { toPng } from 'html-to-image';
import { jsPDF } from 'jspdf';

import { 
  Users, ShieldCheck, Activity, BarChart3, Plus, 
  CheckCircle2, XCircle, Clock, ChevronRight, LogOut, FileText,
  PieChart, TrendingUp, AlertCircle, Network, BookOpen,
  HeartPulse, Smile, Sparkles, ClipboardList, LayoutDashboard, UserSquare2, Star,
  ShieldAlert, Lightbulb, UserCheck, HelpCircle, BarChart2, Layers, RefreshCw, Database, Download, Terminal,
  Brain, Gamepad2, Zap, ShieldOff, Footprints, Flame, Bot, Printer, X
} from 'lucide-react';

import { GAS_URL, gasRequest, getFirestore, doc, setDoc, getDoc, getDocs, onSnapshot, addDoc, updateDoc, deleteDoc, collection } from './lib/gasDb';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell,
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, AreaChart, Area
} from 'recharts';



// --- Firebase Initialization ---

const db = getFirestore();
const appId = '31b45e5f-9483-4bc1-95a4-d5229107671f';

// --- ST-5 Configuration ---
const st5Questions = [
  "มีปัญหาการนอน นอนไม่หลับหรือนอนมากเกินไป",
  "สมาธิน้อยลง",
  "หงุดหงิด/กระวนกระวาย/ว้าวุ่นใจ",
  "รู้สึกเบื่อ เซ็ง",
  "ไม่อยากพบปะผู้คน"
];

const st5Options = [
  { label: "แทบไม่มี (0)", value: 0 },
  { label: "เป็นบางครั้ง (1)", value: 1 },
  { label: "บ่อยครั้ง (2)", value: 2 },
  { label: "เป็นประจำ (3)", value: 3 }
];

const calculateST5 = (score) => {
  if (score <= 4) {
    return { 
      level: 'เครียดน้อย', color: 'bg-teal-50 text-teal-700 border-teal-200', badge: 'bg-teal-500', risk: 'Low',
      guideUser: [
        "รักษาสุขภาพใจให้สดชื่นเช่นนี้ต่อไป นอนหลับพักผ่อนให้เพียงพอ 7-8 ชั่วโมงต่อวัน",
        "หากิจกรรมผ่อนคลายที่ชอบทำเป็นประจำ เช่น ออกกำลังกาย ฟังเพลง ดูหนัง",
        "หมั่นสังเกตอารมณ์และความรู้สึกของตนเองอย่างสม่ำเสมอ"
      ],
      guideAdmin: [
        "ให้คำชื่นชมและส่งเสริมกิจกรรมเชิงบวกเพื่อรักษาเสถียรภาพทางอารมณ์",
        "จัดกิจกรรมพัฒนาทักษะชีวิต (Life Skills) ร่วมกับกลุ่มเพื่อนตามปกติ",
        "เฝ้าระวังทั่วไปตามระบบดูแลช่วยเหลือนักเรียน"
      ]
    };
  }
  if (score <= 7) {
    return { 
      level: 'เครียดปานกลาง', color: 'bg-amber-50 text-amber-700 border-amber-200', badge: 'bg-amber-400', risk: 'Medium',
      guideUser: [
        "ฝึกเทคนิคการผ่อนคลายความเครียด เช่น การฝึกหายใจลึกๆ (4-4-8) หรือการทำสมาธิเบื้องต้น",
        "พูดคุยระบายความรู้สึกกับเพื่อนสนิท ครอบครัว หรือคุณครูที่ไว้วางใจ ไม่เก็บไว้คนเดียว",
        "จำกัดเวลาการใช้สื่อโซเชียลมีเดียที่อาจกระตุ้นความรู้สึกเชิงลบ"
      ],
      guideAdmin: [
        "ให้คำปรึกษาเบื้องต้น (Counseling) ในพื้นที่ส่วนตัวที่เป็นมิตรและปลอดภัย",
        "ใช้หลัก 3L: Look (มองหาความผิดปกติ) Listen (รับฟังอย่างตั้งใจไม่ตัดสิน) Link (เชื่อมโยงผู้ช่วย)",
        "นัดหมายติดตามผลความเครียดซ้ำภายใน 1-2 สัปดาห์"
      ]
    };
  }
  if (score <= 9) {
    return { 
      level: 'เครียดมาก', color: 'bg-rose-50 text-rose-700 border-rose-200', badge: 'bg-rose-400', risk: 'High',
      guideUser: [
        "ควรเข้ารับการคำปรึกษาจากคุณครูแนะแนว หรือบุคลากรสาธารณสุขประจำโครงการโดยด่วน",
        "อนุญาตให้ตัวเองหยุดพักจากแรงกดดันรอบตัวชั่วคราว และหลีกเลี่ยงการตัดสินใจเรื่องสำคัญขณะเครียด",
        "ใช้แอปพลิเคชันช่วยเหลือจิตใจเบื้องต้น หรือปรึกษาแพทย์หากมีอาการทางกาย เช่น ปวดหัวรุนแรง"
      ],
      guideAdmin: [
        "เชิญนักเรียนพูดคุยเป็นการส่วนตัวทันที และประสานงานร่วมกับครูแนะแนว/ครูฝ่ายปกครอง",
        "ประเมินความเสี่ยงเชิงลึกเพิ่มเติมด้วยแบบประเมินภาวะซึมเศร้า (9Q) และการทำร้ายตนเอง (8Y)",
        "แจ้งและปรึกษาผู้ปกครองด้วยท่าทีที่แสดงความห่วงใยร่วมมือ เพื่อหาทางออกร่วมกัน"
      ]
    };
  }
  return { 
    level: 'เครียดมากที่สุด', color: 'bg-red-50 text-red-700 border-red-200', badge: 'bg-red-500', risk: 'Severe',
    guideUser: [
      "ติดต่อโทรสายด่วนสุขภาพจิต 1323 (โทรฟรีตลอด 24 ชั่วโมง) เพื่อรับการประคับประคองใจทันที",
      "บอกผู้ปกครอง หรือบุคคลใกล้ชิดที่สุดให้ทราบ เพื่อคอยช่วยเหลือและอยู่เป็นเพื่อน",
      "แนะนำให้เข้ารับการประเมินและดูแลจากจิตแพทย์หรือแพทย์ผู้เชี่ยวชาญเพื่อความปลอดภัย"
    ],
    guideAdmin: [
      "เข้าสู่กระบวนการเผชิญเหตุวิกฤต (Crisis Intervention) ทันที ห้ามปล่อยให้นักเรียนอยู่คนเดียว",
      "ส่งต่อ (Refer) ไปยังโรงพยาบาลหรือเครือข่ายสาธารณสุขในพื้นที่ตามมาตรการ Mini Flag Ship Satun",
      "แจ้งผู้ปกครองอย่างเป็นทางการและดูแลความปลอดภัยของนักเรียนอย่างใกล้ชิดขั้นสูงสุด"
    ]
  };
};

const behaviors = {
  desirable: [
    { cat: "ด้านการพัฒนาตนเองและสติปัญญา", items: ["การใฝ่เรียนรู้", "การคิดวิเคราะห์", "การแก้ปัญหา"] },
    { cat: "ด้านอารมณ์และจิตใจ", items: ["การควบคุมอารมณ์", "ความเห็นอกเห็นใจผู้อื่น", "ความภาคภูมิใจในตนเอง"] },
    { cat: "ด้านสังคมและจริยธรรม", items: ["ความรับผิดชอบและวินัย", "การเคารพสิทธิผู้อื่น", "จิตสาธารณะ"] },
    { cat: "ด้านสุขภาพและอนามัย", items: ["การดูแลสุขภาพกาย"] }
  ],
  undesirable: [
    { cat: "พฤติกรรมการใช้ความรุนแรง", items: ["การใช้ความรุนแรงและรังแกกัน (Bullying)", "การก่อความเดือดร้อนรำคาญ"] },
    { cat: "พฤติกรรมเสี่ยงและผิดกฎหมาย", items: ["การใช้สารเสพติด", "การพนัน", "พฤติกรรมทางเพศที่ไม่ปลอดภัย"] },
    { cat: "ปัญหาด้านสุขภาพจิตและอารมณ์", items: ["ภาวะซึมเครียดและวิตกกังวล", "อารมณ์ฉุนเฉียวและก้าวร้าว"] },
    { cat: "พฤติกรรมการหลบเลี่ยงหน้าที่", items: ["การหนีเรียน", "พฤติกรรมถดถอยในการเรียน"] },
    { cat: "การติดสื่อและเทคโนโลยี", items: ["การหมกมุ่นกับสื่อออนไลน์"] }
  ]
};

const schoolOptions = [
  "โรงเรียนควนโดนวิทยา", "โรงเรียนอนุบาลท่าแพพัฒนา", "โรงเรียนทุ่งหว้าวรวิทย์",
  "โรงเรียนพัฒนาการมูลนิธิ", "โรงเรียนบ้านดาหลำ", "โรงเรียนละงูพิทยาคม",
  "โรงเรียนท่าแพผดุงวิทย์", "โรงเรียนบ้านวังปริง"
];
const communityOptions = [
  "ชุมชนเพื่อน้องสุขใจ (เกตรี)", "ชุมชนเพื่อน้องสุขใจ (แป-ระ)"
];

const getAffiliationOptions = (accountType) => {
  if (['student', 'teacher', 'admin'].includes(accountType)) return [...schoolOptions, ...communityOptions];
  if (accountType === 'community') return communityOptions;
  if (accountType === 'superadmin') return [...schoolOptions, ...communityOptions];
  return [];
};

const getRoleFromAccountType = (type) => {
  if (['student', 'community', 'teacher'].includes(type)) return 'user';
  if (type === 'admin') return 'admin';
  if (type === 'superadmin') return 'superadmin';
  return 'user';
};

const displayAffiliation = (aff) => {
  if (!aff) return '';
  if (Array.isArray(aff)) return aff.join(', ');
  return aff;
};

// Google Sheets Integration

const syncToGoogleSheet = async (type: string, payload: any) => {
  // DB is now handled natively via gasDb.ts
};

const calculatePearsonCorrelation = (x, y) => {
  let n = x.length;
  if (n <= 1 || y.length === 0 || n !== y.length) return 0; // แก้ไขเพื่อป้องกัน NaN กรณีเลือกดูคนเดียว
  let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0, sumY2 = 0;
  for (let i = 0; i < n; i++) {
    sumX += x[i]; sumY += y[i]; sumXY += x[i] * y[i];
    sumX2 += x[i] * x[i]; sumY2 += y[i] * y[i];
  }
  let numerator = (n * sumXY) - (sumX * sumY);
  let denominator = Math.sqrt(Math.max(0, n * sumX2 - sumX * sumX) * Math.max(0, n * sumY2 - sumY * sumY));
  if (denominator === 0 || isNaN(denominator)) return 0;
  return numerator / denominator;
};

const parseSheetDate = (dateStr) => {
  if(!dateStr) return Date.now();
  try {
      if (typeof dateStr === 'number') return dateStr;
      const StringDate = String(dateStr);
      const parts = StringDate.split(' ');
      if (parts.length >= 2) {
         const [d, t] = parts;
         const [day, mo, yr] = d.split('/');
         const [h, m, s] = t.split(':');
         return new Date(Number(yr), Number(mo)-1, Number(day), Number(h), Number(m), Number(s)).getTime();
      }
      return new Date(StringDate).getTime() || Date.now();
  } catch(e) {
      return Date.now();
  }
};

// ==========================================
// MAIN APP COMPONENT
// ==========================================
export default function App() {
  const [profile, setProfile] = useState(null);
  
  
  const [loading, setLoading] = useState(true);
  const [usersList, setUsersList] = useState([]);
  const [st5Data, setSt5Data] = useState([]);
  const [behaviorData, setBehaviorData] = useState([]);
  const [activeTab, setActiveTab] = useState('dashboard');
  
  // Custom Modals State
  const [alertConfig, setAlertConfig] = useState({ isOpen: false, message: '', type: 'success' });
  const [confirmConfig, setConfirmConfig] = useState({ isOpen: false, message: '', type: 'info', onConfirm: null });

  const triggerAlert = (message, type = 'success') => {
    setAlertConfig({ isOpen: true, message, type });
  };

  const triggerConfirm = (message, onConfirmCallback, type = 'info') => {
    setConfirmConfig({
      isOpen: true,
      message,
      type,
      onConfirm: () => {
        setConfirmConfig({ ...confirmConfig, isOpen: false });
        if (onConfirmCallback) onConfirmCallback();
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
  };

  useEffect(() => {
    const link = document.createElement('link');
    link.href = 'https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&display=swap';
    link.rel = 'stylesheet';
    link.crossOrigin = 'anonymous';
    document.head.appendChild(link);
    return () => document.head.removeChild(link);
  }, []);

  useEffect(() => {
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
  }, []);

  useEffect(() => {
    if (!profile) return;
    const baseUsersRef = collection(db, 'artifacts', appId, 'public', 'data', 'users');
    const st5Ref = collection(db, 'artifacts', appId, 'public', 'data', 'st5');
    const behaviorRef = collection(db, 'artifacts', appId, 'public', 'data', 'behaviors');

    const unsubUsers = onSnapshot(baseUsersRef, (snap) => {
      const users = snap.docs.map(d => ({ id: d.id, ...d.data() }));
      setUsersList(users);
      const updatedProfile = users.find(u => u.id === profile.id);
      if (updatedProfile) setProfile(updatedProfile);
    });
    const unsubSt5 = onSnapshot(st5Ref, (snap) => {
      setSt5Data(snap.docs.map(d => ({ id: d.id, ...d.data() } as any)).sort((a: any, b: any) => b.timestamp - a.timestamp));
    });
    const unsubBehavior = onSnapshot(behaviorRef, (snap) => {
      setBehaviorData(snap.docs.map(d => ({ id: d.id, ...d.data() } as any)).sort((a: any, b: any) => b.timestamp - a.timestamp));
    });
    return () => { unsubUsers(); unsubSt5(); unsubBehavior(); };
  }, [profile?.id]);

  const handleLogin = (userProfile) => {
    localStorage.setItem(`${appId}_session`, userProfile.id);
    setProfile(userProfile);
    triggerAlert('เข้าสู่ระบบสำเร็จแล้ว ยินดีต้อนรับค่ะ ✦', 'success');
  };
  const handleLogout = () => {
    localStorage.removeItem(`${appId}_session`);
    setProfile(null);
    triggerAlert('ออกจากระบบเรียบร้อยแล้วค่ะ ไว้พบกันใหม่นะ', 'success');
  };

  if (loading) {
    return <div style={{fontFamily: "'Kanit', sans-serif"}} className="flex h-screen items-center justify-center bg-purple-50 text-purple-500 text-lg font-medium tracking-wide"><Sparkles className="animate-spin mr-2"/> กำลังโหลดความสดใส...</div>;
  }

  if (!profile) {
    return (
      <div style={{fontFamily: "'Kanit', sans-serif"}}>
        <AuthContainer onLogin={handleLogin} triggerAlert={triggerAlert} />
        <CuteAlert isOpen={alertConfig.isOpen} message={alertConfig.message} type={alertConfig.type} onClose={() => setAlertConfig({ ...alertConfig, isOpen: false })} />
      </div>
    );
  }

  return (
    <div style={{fontFamily: "'Kanit', sans-serif"}} className="min-h-screen bg-[#fdfbf7] flex flex-col md:flex-row font-kanit text-slate-700">
      
      {/* Sidebar */}
      <div className="w-full md:w-72 bg-white md:bg-white/80 backdrop-blur-xl md:h-screen flex flex-col shadow-[4px_0_24px_rgba(236,72,153,0.05)] z-20 border-r border-pink-50/50">
        <div className="p-5 md:p-8 flex items-center justify-between md:justify-start gap-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-gradient-to-br from-pink-300 to-purple-400 rounded-2xl flex items-center justify-center shadow-lg shadow-pink-200 text-white transform -rotate-3">
              <HeartPulse size={26} strokeWidth={2.5}/>
            </div>
            <div>
              <h1 className="text-xl md:text-2xl font-bold text-slate-800 tracking-tight leading-none">Mental Care</h1>
              <span className="text-[11px] md:text-xs font-medium text-purple-400">คัดกรองจิต & ประเมินพฤติกรรม</span>
            </div>
          </div>
          <button onClick={handleLogout} className="md:hidden p-2 text-slate-400 hover:text-rose-400 bg-slate-50 rounded-full">
            <LogOut size={20} />
          </button>
        </div>
        
        <div className="hidden md:block mx-6 mb-6 p-5 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-3xl border border-white shadow-sm">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center text-purple-500 font-bold shadow-sm">
              <Smile size={20}/>
            </div>
            <div className="overflow-hidden">
              <p className="font-bold text-slate-700 truncate">{profile.name}</p>
              <p className="text-[11px] text-slate-500 font-mono truncate">@{profile.id}</p>
            </div>
          </div>
          {profile.affiliation && (
            <p className="text-[11px] text-slate-600 bg-white/60 px-2 py-1.5 rounded-lg truncate" title={displayAffiliation(profile.affiliation)}>
              📍 {displayAffiliation(profile.affiliation)}
            </p>
          )}
          <div className="mt-3 flex">
             <span className={`px-3 py-1 text-[10px] font-bold rounded-full border ${
              profile.role === 'superadmin' ? 'bg-purple-100 text-purple-700 border-purple-200' : 
              profile.role === 'admin' ? 'bg-sky-100 text-sky-700 border-sky-200' : 'bg-teal-100 text-teal-700 border-teal-200'
            }`}>
              {profile.accountType === 'student' ? 'นักเรียน' :
               profile.accountType === 'community' ? 'ชุมชน' :
               profile.accountType === 'teacher' ? 'ครู' :
               profile.accountType === 'admin' ? 'ครู/ผู้รับผิดชอบ' :
               profile.accountType === 'superadmin' ? 'พี่เลี้ยงโครงการ' : profile.role}
            </span>
          </div>
        </div>

        <nav className="flex-none md:flex-1 overflow-x-auto md:overflow-y-auto px-4 md:px-6 pb-4 md:pb-0 hide-scrollbar">
          <div className="flex flex-row md:flex-col gap-2 md:gap-3 min-w-max md:min-w-0">
            <button 
              onClick={() => setActiveTab('dashboard')}
              className={`px-5 py-3.5 rounded-2xl flex items-center gap-3 transition-all font-medium text-sm md:text-base ${
                activeTab === 'dashboard' 
                  ? 'bg-purple-500 text-white shadow-md shadow-purple-200' 
                  : 'bg-white text-slate-500 hover:bg-purple-50 hover:text-purple-600 border border-slate-100'
              }`}
            >
              {profile.role === 'user' ? <UserSquare2 size={20} /> : profile.role === 'admin' ? <ClipboardList size={20} /> : <LayoutDashboard size={20} />} 
              <span>
                {profile.role === 'user' ? 'พื้นที่ของฉัน' : profile.role === 'admin' ? 'รายชื่อและประเมิน' : 'ภาพรวมระบบ'}
              </span>
            </button>

            {(profile.role === 'admin' || profile.role === 'superadmin') && profile.status === 'approved' && (
               <button 
                  onClick={() => setActiveTab('analytics')}
                  className={`px-5 py-3.5 rounded-2xl flex items-center gap-3 transition-all font-medium text-sm md:text-base ${
                    activeTab === 'analytics' 
                      ? 'bg-pink-400 text-white shadow-md shadow-pink-200' 
                      : 'bg-white text-slate-500 hover:bg-pink-50 hover:text-pink-500 border border-slate-100'
                  }`}
               >
                 <Sparkles size={20} /> <span>รายงานวิเคราะห์ข้อมูล</span>
               </button>
            )}

            {/* เมนู Sync (เฉพาะ Superadmin และ Username: rung เท่านั้น) */}
            {profile.role === 'superadmin' && profile.id === 'rung' && (
               <button 
                  onClick={() => setActiveTab('sync')}
                  className={`px-5 py-3.5 rounded-2xl flex items-center gap-3 transition-all font-medium text-sm md:text-base ${
                    activeTab === 'sync' 
                      ? 'bg-indigo-500 text-white shadow-md shadow-indigo-200' 
                      : 'bg-white text-slate-500 hover:bg-indigo-50 hover:text-indigo-600 border border-slate-100'
                  }`}
               >
                 <RefreshCw size={20} /> <span>ซิงก์ข้อมูล (Sync)</span>
               </button>
            )}
          </div>
        </nav>
        
        <div className="hidden md:block p-6">
          <button onClick={handleLogout} className="w-full py-3.5 flex items-center justify-center gap-2 text-slate-500 hover:text-rose-500 hover:bg-rose-50 rounded-2xl transition font-medium text-sm">
            <LogOut size={18} /> ออกจากระบบ
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 p-4 md:p-8 lg:p-10 overflow-y-auto bg-slate-50/50">
        {profile.status === 'pending' ? (
          <div className="bg-orange-50 p-10 rounded-[2.5rem] border border-orange-100 text-center shadow-sm max-w-md mx-auto mt-10 md:mt-20">
            <div className="w-20 h-20 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-6 text-orange-400">
               <Clock size={40} />
            </div>
            <h2 className="text-2xl font-bold text-orange-700 mb-3">รอการอนุมัติสิทธิ์</h2>
            <p className="text-orange-600/80 leading-relaxed text-sm">บัญชีผู้ใช้งานของคุณกำลังรอการอนุมัติจากพี่เลี้ยงโครงการ โปรดรอสักครู่</p>
          </div>
        ) : (
          <div className="max-w-7xl mx-auto space-y-6 md:space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            {activeTab === 'dashboard' && profile.role === 'user' && <UserDashboard users={usersList} profile={profile} st5Data={st5Data} behaviorData={behaviorData} triggerAlert={triggerAlert} triggerConfirm={triggerConfirm} />}
            {activeTab === 'dashboard' && profile.role === 'admin' && <AdminDashboard users={usersList} st5Data={st5Data} behaviorData={behaviorData} profile={profile} triggerAlert={triggerAlert} triggerConfirm={triggerConfirm} triggerDownloadConsentPdf={triggerDownloadConsentPdf} />}
            {activeTab === 'dashboard' && profile.role === 'superadmin' && <SuperAdminDashboard users={usersList} st5Data={st5Data} behaviorData={behaviorData} profile={profile} triggerAlert={triggerAlert} triggerConfirm={triggerConfirm} triggerDownloadConsentPdf={triggerDownloadConsentPdf} />}
            {activeTab === 'analytics' && (profile.role === 'admin' || profile.role === 'superadmin') && (
              <ExecutiveAnalyticsDashboard users={usersList} st5Data={st5Data} behaviorData={behaviorData} profile={profile} />
            )}
            {activeTab === 'sync' && profile.role === 'superadmin' && profile.id === 'rung' && (
              <SyncDashboard triggerAlert={triggerAlert} triggerConfirm={triggerConfirm} st5Data={st5Data} behaviorData={behaviorData} />
            )}
          </div>
        )}
      </div>

      {/* Reusable Cute Modals Overlay */}
      <CuteAlert isOpen={alertConfig.isOpen} message={alertConfig.message} type={alertConfig.type} onClose={() => setAlertConfig({ ...alertConfig, isOpen: false })} />
      <ConfirmModal isOpen={confirmConfig.isOpen} message={confirmConfig.message} type={confirmConfig.type} onConfirm={confirmConfig.onConfirm} onCancel={() => setConfirmConfig({ ...confirmConfig, isOpen: false })} />

      <style dangerouslySetInnerHTML={{__html: `
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
}

// ==========================================
// CUTE MODAL POPUP COMPONENTS
// ==========================================
function CuteAlert({ isOpen, message, type = 'success', onClose }) {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="w-full max-w-sm bg-white p-6 md:p-8 rounded-[2.5rem] shadow-2xl border border-slate-100 text-center space-y-5 animate-in zoom-in-95 duration-300">
        <div className="mx-auto w-20 h-20 rounded-full flex items-center justify-center shadow-lg transform scale-105">
          {type === 'success' ? (
            <div className="w-20 h-20 bg-teal-50 rounded-full flex items-center justify-center text-teal-500 border-2 border-teal-100">
              <CheckCircle2 size={40} className="animate-bounce" />
            </div>
          ) : (
            <div className="w-20 h-20 bg-rose-50 rounded-full flex items-center justify-center text-rose-500 border-2 border-rose-100">
              <AlertCircle size={40} className="animate-pulse" />
            </div>
          )}
        </div>
        <div>
          <h4 className="text-xl font-black text-slate-800">{type === 'success' ? 'สำเร็จเรียบร้อย! ✦' : 'แจ้งเตือน'}</h4>
          <p className="text-sm font-medium text-slate-500 leading-relaxed mt-2 whitespace-pre-line">{message}</p>
        </div>
        <button 
          onClick={onClose}
          className="w-full py-4 bg-gradient-to-r from-purple-400 to-pink-400 text-white rounded-3xl font-bold hover:opacity-95 transition shadow-lg shadow-pink-100 text-sm tracking-wide"
        >
          ตกลง
        </button>
      </div>
    </div>
  );
}

function ConfirmModal({ isOpen, message, type = 'info', onConfirm, onCancel }) {
  if (!isOpen) return null;
  const isDanger = type === 'danger';
  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="w-full max-w-sm bg-white p-6 md:p-8 rounded-[2.5rem] shadow-2xl border border-slate-100 text-center space-y-5 animate-in zoom-in-95 duration-300">
        <div className={`mx-auto w-20 h-20 rounded-full flex items-center justify-center shadow-lg transform scale-105 ${isDanger ? 'bg-rose-50 text-rose-500 border-2 border-rose-100' : 'bg-indigo-50 text-indigo-500 border-2 border-indigo-100'}`}>
          {isDanger ? <AlertCircle size={40} className="animate-pulse" /> : <HelpCircle size={40} className="animate-pulse" />}
        </div>
        <div>
          <h4 className={`text-xl font-black ${isDanger ? 'text-rose-600' : 'text-slate-800'}`}>ยืนยันการดำเนินการ</h4>
          <p className="text-sm font-medium text-slate-500 leading-relaxed mt-2 whitespace-pre-line">{message}</p>
        </div>
        <div className="flex gap-3">
          <button 
            onClick={onCancel}
            className="flex-1 py-3.5 bg-slate-100 text-slate-500 rounded-3xl font-bold hover:bg-slate-200 transition text-sm"
          >
            ยกเลิก
          </button>
          <button 
            onClick={onConfirm}
            className={`flex-1 py-3.5 text-white rounded-3xl font-bold transition shadow-lg text-sm ${isDanger ? 'bg-rose-500 hover:bg-rose-600 shadow-rose-100' : 'bg-indigo-500 hover:bg-indigo-600 shadow-indigo-100'}`}
          >
            ยืนยัน
          </button>
        </div>
      </div>
    </div>
  );
}

// ==========================================
// CONSENT DOCUMENT FOR PRINTING & VIEWING
// ==========================================
function ConsentDocument({ name, dateStr, hidePrintBtn = false, onPrint }) {
  return (
    <div style={{ fontFamily: "'Kanit', sans-serif" }} className="bg-white p-8 md:p-12 font-kanit text-slate-800 max-w-4xl mx-auto shadow-sm border border-slate-200">
       <h1 className="text-center font-bold text-xl md:text-2xl mb-2">เอกสารแสดงความยินยอม (Consent Form) (สำหรับบุคคลทั่วไป)</h1>
       <h2 className="text-center font-bold text-lg md:text-xl mb-2 bg-slate-100 p-2 rounded-lg">แบบแสดงความยินยอม (Consent Form)</h2>
       <p className="font-bold mb-6 text-center text-purple-700">ภายใต้โครงการ Mini Flag Ship Satun</p>

       <p className="mb-4 indent-8 leading-relaxed">
         ข้าพเจ้าทราบดีว่าผู้รับทุนจำเป็นต้องเก็บรวบรวม ใช้ หรือเปิดเผย (ซึ่งต่อไปในเอกสารนี้เรียกว่า “ประมวลผล”) ข้อมูลส่วนบุคคลของข้าพเจ้า โดยมีรายละเอียดดังนี้
       </p>
       <div className="mb-6 pl-4 md:pl-8">
         <p className="font-bold mb-2">1. วัตถุประสงค์ในการขอความยินยอม</p>
         <p className="leading-relaxed text-sm md:text-base">
           เก็บข้อมูลส่วนบุคคล ได้แก่ ชื่อ สกุล ที่อยู่ ประวัติการประเมินสุขภาพจิต และอื่นๆที่เกี่ยวข้อง สำหรับใช้ในการดำเนินงานโครงการดังกล่าว เพื่อนำมาวิเคราะห์ข้อมูล และออกแบบกิจกรรมให้เหมาะสมกับท่านในปรับเปลี่ยนพฤติกรรมให้มีสุขภาพที่ดีขึ้น
         </p>
       </div>

       <div className="flex flex-col sm:flex-row justify-center gap-4 sm:gap-12 mb-8 font-bold bg-purple-50 p-6 rounded-2xl border border-purple-100">
         <div className="flex items-center gap-3">
           <div className="w-6 h-6 border-2 border-black flex items-center justify-center bg-white rounded-sm">
             <span className="text-xl leading-none font-black text-black">✓</span>
           </div>
           <span>ข้าพเจ้าให้ความยินยอม</span>
         </div>
         <div className="flex items-center gap-3 opacity-50">
           <div className="w-6 h-6 border-2 border-black bg-white rounded-sm"></div>
           <span>ข้าพเจ้าไม่ให้ความยินยอม</span>
         </div>
       </div>

       <p className="mb-4 indent-8 leading-relaxed text-sm md:text-base">
         ทั้งนี้ ก่อนการแสดงเจตนาในครั้งนี้ ข้าพเจ้าได้อ่านรายละเอียดจากเอกสารชี้แจงข้อมูลหรือได้รับคำอธิบายถึงวัตถุประสงค์ในการประมวลผลข้อมูลส่วนบุคคลของข้าพเจ้าโดยละเอียดและมีความเข้าใจเป็นอย่างดีแล้ว และข้าพเจ้าได้ให้ความยินยอมหรือปฏิเสธไม่ให้ความยินยอมในเอกสารฉบับนี้ด้วยความสมัครใจโดยปราศจากการบังคับหรือชักจูง
       </p>
       <p className="mb-4 indent-8 leading-relaxed text-sm md:text-base">
         ข้าพเจ้าทราบว่าสามารถถอนความยินยอมนี้เสียเมื่อใดก็ได้ เว้นแต่ในกรณีที่มีข้อจำกัดสิทธิตามกฎหมาย และข้าพเจ้าทราบว่าการถอนความยินยอมนี้ไม่มีผลกระทบต่อการประมวลผลข้อมูลส่วนบุคคลของข้าพเจ้าที่ได้ดำเนินการเสร็จสิ้นไปแล้วก่อนการถอนความยินยอม
       </p>
       <p className="mb-12 indent-8 leading-relaxed text-sm md:text-base font-bold text-slate-700">
         ข้าพเจ้าได้อ่านเอกสารฉบับนี้โดยละเอียดและมีความเข้าใจเป็นอย่างดีแล้วจึงได้ลงลายมือชื่อไว้เป็นหลักฐาน
       </p>

       <div className="flex flex-col items-center mt-12 sm:w-2/3 ml-auto text-sm md:text-base">
         <div className="flex items-end mb-4 w-full">
            <span className="whitespace-nowrap mr-2">(ลงชื่อ)</span>
            <div className="flex-1 border-b border-black border-dashed text-center font-bold text-lg text-purple-700 font-handwriting pb-1 px-4">{name || '...........................................'}</div>
            <span className="whitespace-nowrap ml-2">ผู้เข้าร่วมกิจกรรม/เจ้าของข้อมูลส่วนบุคคล</span>
         </div>
         <div className="flex items-end mb-4 w-full justify-center">
            <span className="whitespace-nowrap mr-2">(</span>
            <div className="w-64 text-center font-medium">{name || '...........................................'}</div>
            <span className="whitespace-nowrap ml-2">)</span>
         </div>
         <div className="flex items-end w-full justify-center">
            <span className="whitespace-nowrap mr-2">วันที่</span>
            <div className="w-64 border-b border-black border-dashed text-center pb-1">{dateStr || '........./......../.........'}</div>
         </div>
       </div>
       
       {!hidePrintBtn && (
         <div data-html2canvas-ignore="true" className="mt-12 flex justify-center print:hidden border-t border-slate-100 pt-8">
            <button onClick={onPrint} className="bg-purple-600 text-white px-8 py-3 rounded-2xl font-bold flex items-center gap-2 hover:bg-purple-700 transition shadow-lg shadow-purple-200">
               <Printer size={20} /> พิมพ์ / บันทึกเป็น PDF
            </button>
         </div>
       )}
    </div>
  )
}

// ==========================================
// AUTHENTICATION CONTAINERS
// ==========================================
function AuthContainer({ onLogin, triggerAlert }) {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-sky-50 flex flex-col items-center justify-center p-4">
      <div className="mb-8 text-center animate-in zoom-in duration-500">
        <div className="w-24 h-24 bg-white rounded-[2rem] flex items-center justify-center mx-auto mb-6 shadow-xl shadow-purple-200/50 transform rotate-3">
          <HeartPulse className="text-purple-400" size={48} strokeWidth={2} />
        </div>
        <h1 className="text-2xl md:text-3xl font-extrabold text-slate-800 tracking-tight leading-tight">
          Mental Care <br className="hidden sm:block" /> ระบบคัดกรองสุขภาพจิตและประเมินพฤติกรรม
        </h1>
        <p className="text-purple-500 mt-3 font-bold text-lg">พื้นที่แห่งความเข้าใจ ใส่ใจสุขภาพจิต</p>
        <p className="text-sky-600 mt-1 font-medium text-sm">ภายใต้โครงการ Mini Flag Ship Satun</p>
        <p className="text-slate-500 mt-2 text-xs">ผู้จัดทำ นายรุ่งศักดิ์ จอสกุล นักวิชาการสาธารณสุขชำนาญการ</p>
      </div>
      
      <div className="bg-white/80 backdrop-blur-xl p-8 md:p-10 rounded-[3rem] shadow-2xl shadow-purple-200/40 w-full max-w-md border border-white">
        <div className="flex bg-slate-100/80 p-1.5 rounded-3xl mb-8">
          <button 
            className={`flex-1 py-3 text-sm font-bold rounded-[1.25rem] transition-all duration-300 ${isLogin ? 'bg-white shadow-sm text-purple-600' : 'text-slate-400 hover:text-slate-600'}`}
            onClick={() => setIsLogin(true)}
          >
            เข้าสู่ระบบ
          </button>
          <button 
            className={`flex-1 py-3 text-sm font-bold rounded-[1.25rem] transition-all duration-300 ${!isLogin ? 'bg-white shadow-sm text-purple-600' : 'text-slate-400 hover:text-slate-600'}`}
            onClick={() => setIsLogin(false)}
          >
            สร้างบัญชีใหม่
          </button>
        </div>

        {isLogin ? <LoginForm onLoginSuccess={onLogin} /> : <RegisterForm onRegisterSuccess={() => { setIsLogin(true); triggerAlert('สร้างบัญชีผู้ใช้ใหม่เรียบร้อยแล้วค่ะ โปรดเข้าสู่ระบบ', 'success'); }} />}
      </div>
    </div>
  );
}

function LoginForm({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    if (!username || !password) return setError('กรุณากรอกข้อมูลให้ครบถ้วน');
    setLoading(true);
    try {
      const docRef = doc(db, 'artifacts', appId, 'public', 'data', 'users', username.toLowerCase());
      const snap = await getDoc(docRef);
      if (snap.exists() && String(snap.data().password) === String(password)) {
        onLoginSuccess({ id: snap.id, ...snap.data() });
      } else {
        setError('ชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง');
      }
    } catch (err) {
      console.error("Login Error:", err);
      setError(err.message || 'เกิดข้อผิดพลาดในการเชื่อมต่อ');
    }
    setLoading(false);
  };

  return (
    <form onSubmit={handleLogin} className="space-y-5">
      {error && <div className="p-4 bg-rose-50 text-rose-500 text-sm rounded-2xl border border-rose-100 flex items-center gap-2 font-medium"><AlertCircle size={18}/> {error}</div>}
      <div>
        <label className="block text-sm font-bold text-slate-600 mb-2 pl-2">ชื่อผู้ใช้งาน</label>
        <input 
          type="text" 
          className="w-full p-4 border border-slate-200 rounded-3xl focus:ring-4 focus:ring-purple-500/20 focus:border-purple-400 outline-none bg-white transition-all text-sm"
          value={username} onChange={e => setUsername(e.target.value)} placeholder="Username"
        />
      </div>
      <div>
        <label className="block text-sm font-bold text-slate-600 mb-2 pl-2">รหัสผ่าน</label>
        <input 
          type="password" 
          className="w-full p-4 border border-slate-200 rounded-3xl focus:ring-4 focus:ring-purple-500/20 focus:border-purple-400 outline-none bg-white transition-all text-sm"
          value={password} onChange={e => setPassword(e.target.value)} placeholder="Password"
        />
      </div>
      <button 
        type="submit" disabled={loading}
        className="w-full bg-gradient-to-r from-purple-400 to-pink-400 text-white p-4 rounded-3xl font-bold hover:opacity-90 disabled:opacity-50 transition-all shadow-lg shadow-pink-200 mt-6 text-base"
      >
        {loading ? 'กำลังโหลด...' : 'เริ่มต้นใช้งาน ✦'}
      </button>
    </form>
  );
}

function RegisterForm({ onRegisterSuccess }) {
  const [formData, setFormData] = useState({ 
    username: '', password: '', name: '', accountType: 'student', affiliation: schoolOptions[0] 
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [showConsent, setShowConsent] = useState(false);
  const [isConsented, setIsConsented] = useState(false);
  const [registeredUser, setRegisteredUser] = useState(null);

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    if (!formData.username || !formData.password || !formData.name) return setError('กรุณากรอกข้อมูลให้ครบถ้วน');
    if (!isConsented) return setError('กรุณาอ่านและกดยอมรับเอกสารความยินยอม (Consent Form) ก่อนสร้างบัญชี');
    
    setLoading(true);
    try {
      const usernameKey = formData.username.toLowerCase();
      const docRef = doc(db, 'artifacts', appId, 'public', 'data', 'users', usernameKey);
      const snap = await getDoc(docRef);
      
      if (snap.exists()) {
        setError('ชื่อนี้มีคนใช้แล้วจ้า ลองชื่ออื่นดูนะ');
      } else {
        const role = getRoleFromAccountType(formData.accountType);
        const userData = { ...formData, role, status: role === 'admin' ? 'pending' : 'approved', createdAt: Date.now() };
        await setDoc(docRef, userData);
        syncToGoogleSheet('REGISTER', { username: usernameKey, ...userData });
        setSuccess('สร้างบัญชีสำเร็จ! กรุณาพิมพ์หรือบันทึกเอกสารความยินยอมก่อนเข้าสู่ระบบ');
        setRegisteredUser(userData);
      }
    } catch (err) {
      setError(err.message || 'เกิดข้อผิดพลาดในการเชื่อมต่อ');
    }
    setLoading(false);
  };

  const generatePdfFromElement = async (elementId, filename) => {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    // Temporarily make it visible if it's hidden
    const originalStyles = {
      position: element.style.position,
      left: element.style.left,
      top: element.style.top,
      width: element.style.width,
    };
    
    // ensure it's in viewport and rendered
    element.style.position = 'absolute';
    element.style.left = '0';
    element.style.top = '0';
    element.style.width = '800px';
    element.style.zIndex = '-9999';

    try {
      setLoading(true); // Assuming setLoading is accessible in this scope (it is in RegisterForm)
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
      pdf.save(filename); // Still download it locally for the user
      
      // Get base64 string
      const pdfBase64 = pdf.output('datauristring').split(',')[1];
      
      // Upload to Google Drive via Apps Script
      await gasRequest('UPLOAD_PDF', 'Users', { filename: filename, base64: pdfBase64 });
      
      setSuccess('สร้างบัญชีและบันทึก PDF ลง Google Drive สำเร็จ!');
    } catch (err) {
      console.error('Error generating/uploading PDF', err);
      setError('เกิดข้อผิดพลาดในการสร้างหรืออัปโหลด PDF');
    } finally {
      element.style.position = originalStyles.position;
      element.style.left = originalStyles.left;
      element.style.top = originalStyles.top;
      element.style.width = originalStyles.width;
      setLoading(false);
    }
  };

  const handlePrintConsent = () => {
    generatePdfFromElement('consent-success-pdf', `${registeredUser?.name || 'ConsentForm'}.pdf`);
  };

  const handlePrintModal = () => {
    generatePdfFromElement('consent-modal-pdf', `${formData.name || 'ConsentForm'}.pdf`);
  };

  const inputClass = "w-full p-4 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-purple-500/20 focus:border-purple-400 outline-none bg-white transition-all text-sm";
  const labelClass = "block text-xs font-bold text-slate-500 mb-1.5 pl-1";

  if (registeredUser) {
     return (
       <div className="space-y-6 text-center animate-in zoom-in">
         <div className="w-16 h-16 bg-teal-100 rounded-full flex items-center justify-center mx-auto text-teal-600 mb-4">
            <CheckCircle2 size={32} />
         </div>
         <h3 className="text-xl font-bold text-slate-800">สร้างบัญชีสำเร็จ!</h3>
         <p className="text-sm text-slate-500 mb-6 leading-relaxed">
           ระบบได้บันทึกข้อมูลของคุณเรียบร้อยแล้ว<br/>
           กรุณากดปุ่มด้านล่างเพื่อพิมพ์ หรือบันทึกเอกสารแสดงความยินยอม (Consent Form) เป็น PDF
         </p>
         
         <div className="absolute top-[-9999px] left-[-9999px] w-[800px] bg-white text-black">
            <div id="consent-success-pdf">
              <ConsentDocument 
                  name={registeredUser.name} 
                  dateStr={new Date().toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' })}
                  hidePrintBtn={true}
                  onPrint={() => {}}
              />
            </div>
         </div>

         <div className="flex flex-col gap-3">
            <button onClick={handlePrintConsent} className="w-full bg-purple-600 text-white p-4 rounded-3xl font-bold hover:bg-purple-700 transition shadow-md flex items-center justify-center gap-2">
               <Printer size={20} /> พิมพ์ / บันทึก Consent Form
            </button>
            <button onClick={onRegisterSuccess} className="w-full bg-slate-100 text-slate-600 p-4 rounded-3xl font-bold hover:bg-slate-200 transition">
               กลับไปหน้าเข้าสู่ระบบ
            </button>
         </div>
       </div>
     )
  }

  return (
    <>
      <form onSubmit={handleRegister} className="space-y-4">
        {error && <div className="p-3 bg-rose-50 text-rose-500 text-sm rounded-xl border border-rose-100 flex items-center gap-2"><XCircle size={16}/> {error}</div>}
        {success && <div className="p-3 bg-teal-50 text-teal-600 text-sm rounded-xl border border-teal-100 flex items-center gap-2"><CheckCircle2 size={16}/> {success}</div>}
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="md:col-span-2">
            <label className={labelClass}>ชื่อ-นามสกุล</label>
            <input type="text" className={inputClass} value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} placeholder="ชื่อและนามสกุล" />
          </div>
          <div>
            <label className={labelClass}>Username</label>
            <input type="text" className={inputClass} value={formData.username} onChange={e => setFormData({...formData, username: e.target.value.replace(/\s+/g, '')})} placeholder="ภาษาอังกฤษ/ตัวเลข" />
          </div>
          <div>
            <label className={labelClass}>รหัสผ่าน</label>
            <input type="password" className={inputClass} value={formData.password} onChange={e => setFormData({...formData, password: e.target.value})} placeholder="ตั้งรหัสผ่าน" />
          </div>
          <div className="md:col-span-2">
            <label className={labelClass}>คุณคือใคร?</label>
            <select className={inputClass} value={formData.accountType} onChange={e => {
                const newType = e.target.value;
                setFormData({...formData, accountType: newType, affiliation: newType === 'superadmin' ? [] : (getAffiliationOptions(newType)[0] || '')});
              }}>
              <option value="student">นักเรียน</option>
              <option value="community">คนในชุมชน</option>
              <option value="teacher">คุณครู</option>
              <option value="admin">ครู/ผู้รับผิดชอบ (Admin)</option>
              <option value="superadmin">พี่เลี้ยงโครงการ (Superadmin)</option>
            </select>
          </div>
          
          <div className="md:col-span-2">
            <label className={labelClass}>สังกัดอยู่ที่ไหน?</label>
            {formData.accountType === 'superadmin' ? (
              <div className="w-full p-4 border border-slate-200 rounded-2xl bg-white h-32 overflow-y-auto">
                {getAffiliationOptions(formData.accountType).map((opt, idx) => (
                  <label key={idx} className="flex items-start space-x-3 mb-2.5 cursor-pointer group">
                    <input type="checkbox" checked={Array.isArray(formData.affiliation) && formData.affiliation.includes(opt)}
                      onChange={(e) => {
                        const current = Array.isArray(formData.affiliation) ? formData.affiliation : [];
                        setFormData({...formData, affiliation: e.target.checked ? [...current, opt] : current.filter(i => i !== opt)});
                      }}
                      className="mt-0.5 rounded text-purple-500 focus:ring-purple-400 border-slate-300"
                    />
                    <span className="text-sm text-slate-600 group-hover:text-purple-600 transition">{opt}</span>
                  </label>
                ))}
              </div>
            ) : (
              <select className={inputClass} value={formData.affiliation} onChange={e => setFormData({...formData, affiliation: e.target.value})}>
                {getAffiliationOptions(formData.accountType).map((opt, idx) => <option key={idx} value={opt}>{opt}</option>)}
              </select>
            )}
          </div>
        </div>

        <div className="mt-4 p-4 bg-purple-50 rounded-2xl border border-purple-100">
           <label className="flex items-start gap-3 cursor-pointer">
             <input type="checkbox" className="mt-1 w-5 h-5 rounded text-purple-600 focus:ring-purple-500"
                checked={isConsented} onChange={e => setIsConsented(e.target.checked)} />
             <span className="text-sm text-slate-700 leading-relaxed font-medium">
               ข้าพเจ้าได้อ่านและยอมรับ <button type="button" onClick={() => setShowConsent(true)} className="text-purple-600 underline font-bold">เอกสารแสดงความยินยอม (Consent Form)</button> สำหรับการเก็บรวบรวมข้อมูลส่วนบุคคล
             </span>
           </label>
        </div>

        <button type="submit" disabled={loading || success || !isConsented} className="w-full bg-slate-800 text-white p-4 rounded-3xl font-bold hover:bg-slate-700 disabled:bg-slate-300 disabled:cursor-not-allowed transition-all shadow-md mt-6 text-base">
          สร้างบัญชีเลย! ✨
        </button>
      </form>

      {showConsent && (
         <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
            <div className="bg-white w-full max-w-4xl max-h-[90vh] overflow-y-auto rounded-3xl shadow-2xl animate-in zoom-in-95 duration-300 flex flex-col relative">
               <button onClick={() => setShowConsent(false)} className="absolute top-4 right-4 w-10 h-10 bg-slate-100 rounded-full flex items-center justify-center text-slate-500 hover:bg-rose-100 hover:text-rose-500 transition">
                  <X size={20} />
               </button>
               <div id="consent-modal-pdf">
                 <ConsentDocument 
                    name={formData.name} 
                    dateStr={new Date().toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' })}
                    onPrint={handlePrintModal}
                 />
               </div>
               <div className="p-6 md:p-8 bg-slate-50 border-t border-slate-100 flex justify-end gap-4 rounded-b-3xl">
                  <button onClick={() => setShowConsent(false)} className="px-6 py-3 bg-slate-200 text-slate-700 rounded-xl font-bold hover:bg-slate-300 transition">ปิดหน้าต่าง</button>
                  <button onClick={() => { setIsConsented(true); setShowConsent(false); }} className="px-6 py-3 bg-purple-600 text-white rounded-xl font-bold hover:bg-purple-700 shadow-md shadow-purple-200 transition">ฉันยอมรับเงื่อนไข</button>
               </div>
            </div>
         </div>
      )}
    </>
  );
}

// ==========================================
// USER DASHBOARD
// ==========================================
function UserDashboard({ users, profile, st5Data, behaviorData, triggerAlert, triggerConfirm }) {
  const [showST5, setShowST5] = useState(false);
  const myAdmins = users?.filter(u => u.role === 'admin' && u.affiliation === profile.affiliation && u.status === 'approved') || [];
  const projectMentors = users?.filter(u => u.role === 'superadmin') || [];

  const [st5Result, setSt5Result] = useState(null);
  const [editingST5, setEditingST5] = useState(null); 
  const myHistory = st5Data.filter(d => d.uid === profile.id || d.userId === profile.id);

  const handleSubmitST5 = async (answers, score) => {
    const st5Obj = calculateST5(score);
    const payload = { uid: profile.id, userId: profile.id, userName: profile.name, answers, score, level: st5Obj.level, timestamp: editingST5 ? editingST5.timestamp : Date.now(), suggestion: editingST5 ? editingST5.suggestion : '' };
    
    if (editingST5) {
       await updateDoc(doc(db, 'artifacts', appId, 'public', 'data', 'st5', editingST5.id), payload);
       triggerAlert('แก้ไขข้อมูลการคัดกรอง ST-5 เรียบร้อยแล้วค่ะ', 'success');
       setEditingST5(null);
    } else {
       await addDoc(collection(db, 'artifacts', appId, 'public', 'data', 'st5'), payload);
       syncToGoogleSheet('ST5', payload);
       triggerAlert('บันทึกผลการคัดกรอง ST-5 ลงระบบและ Google Sheets เรียบร้อยแล้วค่ะ', 'success');
       setSt5Result({ score, ...st5Obj }); 
    }
    setShowST5(false);
  };


  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:justify-between md:items-end gap-4 bg-white p-6 rounded-[2rem] shadow-sm border border-slate-100">
        <div>
          <h2 className="text-2xl md:text-3xl font-extrabold text-slate-800 tracking-tight flex items-center gap-3">
             <Star className="text-amber-400 fill-amber-400" size={28}/> พื้นที่ของฉัน
          </h2>
          <p className="text-slate-500 text-sm mt-1">ยินดีต้อนรับกลับมานะ สำรวจสุขภาพใจของคุณกันเถอะ</p>
        </div>
        
        <div className="flex-1 w-full md:w-auto mt-4 md:mt-0 flex flex-col md:flex-row gap-3">
           {myAdmins.length > 0 && (
             <div className="bg-sky-50 border border-sky-100 p-3 rounded-2xl flex-1">
                <p className="text-[10px] font-bold text-sky-600 mb-1">ครู/ผู้รับผิดชอบ (Admin)</p>
                <div className="flex flex-wrap gap-2">
                  {myAdmins.map(a => (
                     <span key={a.id} className="text-xs font-medium text-slate-700 bg-white px-2 py-1 rounded-lg border border-sky-100">{a.name}</span>
                  ))}
                </div>
             </div>
           )}
           {projectMentors.length > 0 && (
             <div className="bg-purple-50 border border-purple-100 p-3 rounded-2xl flex-1">
                <p className="text-[10px] font-bold text-purple-600 mb-1">พี่เลี้ยงโครงการ</p>
                <div className="flex flex-wrap gap-2">
                  {projectMentors.map(m => (
                     <span key={m.id} className="text-xs font-medium text-slate-700 bg-white px-2 py-1 rounded-lg border border-purple-100">{m.name}</span>
                  ))}
                </div>
             </div>
           )}
        </div>
        {!showST5 && !st5Result && (
           <button onClick={() => setShowST5(true)} className="bg-gradient-to-r from-sky-400 to-indigo-400 text-white px-6 py-3.5 rounded-2xl text-sm font-bold hover:opacity-90 shadow-lg shadow-sky-200 transition transform hover:-translate-y-0.5">
             + ทำแบบประเมิน ST-5 
           </button>
        )}
      </div>

      {/* POPUP MODAL: แสดงผลลัพธ์ ST-5 ย้อนหลังหรือหลังทำทันที */}
      {st5Result && (
        <ST5ResultModal result={st5Result} isTeacherView={false} onSummaryClose={() => setSt5Result(null)} />
      )}
      
      {showST5 && !st5Result && (
        <ST5Form onSubmit={handleSubmitST5} onCancel={() => { setShowST5(false); setEditingST5(null); }} initialData={editingST5} />
      )}

      {!showST5 && !st5Result && (
        <div className="bg-white p-6 md:p-8 rounded-[2rem] shadow-sm border border-slate-100">
          <h3 className="text-lg font-bold flex items-center gap-2 text-slate-700 mb-6"><FileText className="text-sky-400"/> ประวัติการประเมินของคุณ</h3>
          {myHistory.length === 0 ? (
            <div className="text-center py-16 bg-slate-50/50 rounded-3xl border-2 border-dashed border-slate-200">
              <Smile className="mx-auto text-slate-300 mb-4" size={56} strokeWidth={1.5} />
              <p className="text-slate-500 font-medium">ยังไม่มีข้อมูลเลย ลองทำแบบประเมินครั้งแรกดูสิ</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-sm min-w-[600px]">
                <thead>
                  <tr className="border-b-2 border-slate-100">
                    <th className="p-4 font-bold text-slate-400 uppercase tracking-wider text-xs">ครั้งที่ / วันที่</th>
                    <th className="p-4 font-bold text-slate-400 uppercase tracking-wider text-xs text-center">คะแนนรวม</th>
                    <th className="p-4 font-bold text-slate-400 uppercase tracking-wider text-xs">ระดับความเครียด</th>
                    <th className="p-4 font-bold text-slate-400 uppercase tracking-wider text-xs">ข้อเสนอแนะความห่วงใย</th>
                    <th className="p-4 font-bold text-slate-400 uppercase tracking-wider text-xs text-center">จัดการ</th>
                  </tr>
                </thead>
                <tbody>
                  {myHistory.map((item, idx) => {
                    const status = calculateST5(item.score);
                    return (
                      <tr key={idx} className="border-b border-slate-50 hover:bg-slate-50/50 transition">
                        <td className="p-4">
                          <div className="font-bold text-sky-500">ครั้งที่ {myHistory.length - idx}</div>
                          <div className="text-xs text-slate-400 mt-0.5">{new Date(item.timestamp).toLocaleDateString('th-TH')}</div>
                        </td>
                        <td className="p-4 text-center font-black text-slate-700 text-lg">{item.score}</td>
                        <td className="p-4">
                          <span className={`px-4 py-1.5 rounded-full text-xs font-bold border ${status.color}`}>
                            {item.level || status.level}
                          </span>
                        </td>
                        <td className="p-4">
                          {item.suggestion ? (
                            <div className="bg-indigo-50 border border-indigo-100 p-3 rounded-2xl text-indigo-700 text-sm leading-relaxed">
                              {item.suggestion}
                            </div>
                          ) : (
                            <span className="text-slate-300 italic text-xs">คุณครูกำลังพิจารณาข้อมูล...</span>
                          )}
                        </td>
                        <td className="p-4 text-center">
                          <div className="flex items-center justify-center gap-2">
                            <button onClick={() => { setEditingST5(item); setShowST5(true); }} className="text-xs bg-sky-50 text-sky-600 px-3 py-1.5 border border-sky-200 rounded-full hover:bg-sky-100 transition font-bold shadow-sm">
                              แก้ไข
                            </button>

                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ==========================================
// ACADEMIC REPORT MODAL COMPONENT (ST-5) - TRUE POPUP OVERLAY
// ==========================================
function ST5ResultModal({ result, isTeacherView, onSummaryClose }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-in fade-in duration-200 overflow-y-auto">
      <div className="relative w-full max-w-3xl bg-white border-2 border-purple-100 p-6 md:p-8 rounded-[2.5rem] shadow-2xl space-y-6 my-8 max-h-[90vh] overflow-y-auto custom-scrollbar animate-in zoom-in-95 duration-300">
        
        {/* Close Button Icon */}
        <button 
          onClick={onSummaryClose} 
          className="absolute top-4 right-4 p-2 text-slate-400 hover:text-rose-500 hover:bg-rose-50 rounded-full transition-all"
        >
          <XCircle size={28} />
        </button>

        <div className="flex items-center gap-3 border-b pb-4">
          <div className="w-10 h-10 bg-purple-100 text-purple-600 rounded-xl flex items-center justify-center">
            <Sparkles size={20}/>
          </div>
          <div>
            <h4 className="font-black text-lg text-slate-800">รายงานผลลัพธ์และคู่มือแนวทางตามหลักวิชาการ</h4>
            <p className="text-xs text-slate-400">อ้างอิงหลักเกณฑ์การคัดกรองกรมสุขภาพจิต กระทรวงสาธารณสุข</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center bg-slate-50 p-5 rounded-3xl border border-slate-100">
          <div className="text-center md:border-r border-slate-200 py-2">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">คะแนนรวมความเครียด</p>
            <p className="text-5xl font-black text-slate-800 mt-1">{result.score}</p>
            <p className="text-[11px] text-slate-400 mt-1">(คะแนนเต็ม 15 คะแนน)</p>
          </div>
          <div className="md:col-span-2 px-2 md:px-6">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">ผลประเมินระดับความเครียด</p>
            <div className="flex items-center gap-3 mt-2">
              <span className={`px-4 py-1.5 rounded-full text-sm font-black border ${result.color}`}>
                {result.level}
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-2 leading-relaxed font-medium">
              {result.risk === 'Low' && "ระดับสุขภาพจิตอยู่ในเกณฑ์ปกติ มีความยืดหยุ่นทางอารมณ์ที่ดี ควรสรักษาสุขภาพใจเชิงรุกอย่างต่อเนื่อง"}
              {result.risk === 'Medium' && "พบภาวะความเครียดสะสมปานกลาง อาจมีปัจจัยกระตุ้นชั่วคราว ควรใช้กระบวนการดูแลและผ่อนคลายความตึงเครียด"}
              {result.risk === 'High' && "⚠️ ระดับความเครียดสูง มีผลกระทบต่อระบบสมาธิหรือการดำเนินชีวิต ควรรับคำปรึกษาประคับประคองใจเชิงลึก"}
              {result.risk === 'Severe' && "🚨 วิกฤตสุขภาพใจระดับรุนแรงสูงสุด จำเป็นต้องเข้าสู่ระบบช่วยเหลือส่งต่อทางการแพทย์และการดูแลใกล้ชิด"}
            </p>
          </div>
        </div>

        {/* ควบคุมการแสดงผลตามสิทธิ์ในการมองเห็นแนวทางปฏิบัติ */}
        <div className={`grid grid-cols-1 ${isTeacherView ? 'md:grid-cols-2' : ''} gap-6`}>
          {/* สำหรับผู้รับการประเมิน */}
          <div className="bg-sky-50/50 border border-sky-100 p-5 rounded-3xl space-y-3">
            <h5 className="font-bold text-sky-700 text-sm flex items-center gap-2"><Smile size={18} className="text-sky-500"/> แนวปฏิบัติสำหรับคุณ (ผู้รับการประเมิน)</h5>
            <ul className="text-xs text-slate-600 space-y-2.5 list-none pl-1">
              {result.guideUser.map((g, i) => (
                <li key={i} className="flex items-start gap-2 leading-relaxed">
                  <span className="text-sky-400 font-bold shrink-0 mt-0.5">✦</span> <span>{g}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* แสดงเฉพาะผู้ใช้งานระดับครู/ผู้รับผิดชอบ (Admin, Superadmin) เท่านั้น */}
          {isTeacherView && (
            <div className="bg-purple-50/50 border border-purple-100 p-5 rounded-3xl space-y-3 animate-in fade-in">
              <h5 className="font-bold text-purple-700 text-sm flex items-center gap-2"><UserCheck size={18} className="text-purple-500"/> แนวปฏิบัติสำหรับ คุณครู/ผู้รับผิดชอบ</h5>
              <ul className="text-xs text-slate-600 space-y-2.5 list-none pl-1">
                {result.guideAdmin.map((g, i) => (
                  <li key={i} className="flex items-start gap-2 leading-relaxed">
                    <span className="text-purple-400 font-bold shrink-0 mt-0.5">✔</span> <span className="text-slate-800 font-semibold">{g}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        <div className="flex justify-end pt-2 border-t">
          <button 
            onClick={onSummaryClose}
            className="px-6 py-3 bg-purple-500 hover:bg-purple-600 text-white font-bold rounded-2xl shadow-md transition-all text-sm"
          >
            ตกลงและรับทราบแนวทาง
          </button>
        </div>
      </div>
    </div>
  );
}

// ==========================================
// ACADEMIC REPORT COMPONENT (BEHAVIOR) - TRUE POPUP OVERLAY
// ==========================================
function BehaviorResultSummary({ selections, onSummaryClose }) {
  const desCount = selections.desirable?.length || 0;
  const undCount = selections.undesirable?.length || 0;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-in fade-in duration-200 overflow-y-auto">
      <div className="relative w-full max-w-2xl bg-white border-2 border-teal-100 p-6 md:p-8 rounded-[2.5rem] shadow-2xl space-y-6 my-8 max-h-[90vh] overflow-y-auto custom-scrollbar animate-in zoom-in-95 duration-300">
        
        {/* Close Button Icon */}
        <button 
          onClick={onSummaryClose} 
          className="absolute top-4 right-4 p-2 text-slate-400 hover:text-rose-500 hover:bg-rose-50 rounded-full transition-all"
        >
          <XCircle size={28} />
        </button>

        <div className="flex justify-between items-center border-b pb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-teal-100 text-teal-600 rounded-xl flex items-center justify-center">
              <ClipboardList size={20}/>
            </div>
            <div>
              <h4 className="font-black text-lg text-slate-800">ผลการวิเคราะห์และข้อเสนอแนะเชิงพฤติกรรม</h4>
              <p className="text-xs text-slate-400">กลยุทธ์เสริมสร้างพฤติกรรมเชิงบวกและปรับเปลี่ยนพฤติกรรมเสี่ยง</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="p-4 bg-teal-50/50 border border-teal-100 rounded-2xl text-center">
            <p className="text-xs font-bold text-teal-600 uppercase tracking-wide">พฤติกรรมน่าชื่นชมที่พบ</p>
            <p className="text-3xl font-black text-teal-700 mt-1">{desCount} <span className="text-xs font-normal text-slate-400">รายการ</span></p>
          </div>
          <div className="p-4 bg-rose-50/50 border border-rose-100 rounded-2xl text-center">
            <p className="text-xs font-bold text-rose-600 uppercase tracking-wide">พฤติกรรมเฝ้าระวังที่พบ</p>
            <p className="text-3xl font-black text-rose-700 mt-1">{undCount} <span className="text-xs font-normal text-slate-400">รายการ</span></p>
          </div>
        </div>

        <div className="space-y-4">
          <div className="bg-slate-50 p-5 rounded-3xl border border-slate-100 space-y-2">
            <p className="text-sm font-bold text-slate-700 flex items-center gap-2"><Smile size={16} className="text-teal-500"/> แนวทางปฏิบัติและพัฒนาการสำหรับผู้รับการประเมิน:</p>
            <p className="text-xs text-slate-600 leading-relaxed font-semibold">
              {undCount === 0 
                ? "ยินดีด้วย! คุณมีพัฒนาการและทักษะทางสังคมที่ยอดเยี่ยม รักษาความมีวินัย จิตสาธารณะ และการใฝ่รู้เช่นนี้ไว้ เพื่อเป็นแบบอย่างที่ดีแก่กลุ่มเพื่อนและชุมชนต่อไป"
                : "รับรู้และยอมรับพฤติกรรมบางประการที่อาจส่งผลกระทบต่อการเรียนหรือความสัมพันธ์ พยายามเปิดใจรับฟังคำแนะนำของคุณครู เข้าร่วมกิจกรรมสันทนาการเชิงสร้างสรรค์เพื่อระบายออกทางอารมณ์อย่างถูกวิธี"
              }
            </p>
          </div>

          <div className="bg-indigo-50/50 p-5 rounded-3xl border border-indigo-100 space-y-3">
            <p className="text-sm font-bold text-indigo-700 flex items-center gap-2"><Lightbulb size={16} className="text-indigo-500"/> แนวทางวิชาการและ Action Plan สำหรับ คุณครู/ผู้รับผิดชอบ:</p>
            <div className="text-xs text-slate-600 space-y-2 leading-relaxed pl-1">
              {desCount > 0 && (
                <div className="flex items-start gap-2">
                  <span className="text-teal-500 font-bold">▶</span>
                  <span><strong>การเสริมแรงเชิงบวก (Positive Reinforcement):</strong> ให้การชื่นชมอย่างเฉพาะเจาะจงในพฤติกรรมพึงประสงค์ที่นักเรียนทำสำเร็จ เพื่อกระตุ้นให้เกิดพฤติกรรมดีซ้ำ</span>
                </div>
              )}
              {undCount > 0 && (
                <>
                  <div className="flex items-start gap-2">
                    <span className="text-rose-500 font-bold">▶</span>
                    <span><strong>ปรับเปลี่ยนพฤติกรรม (Behavior Modification):</strong> หลีกเลี่ยงการทำโทษด้วยวิธีรุนแรงหรือประจานต่อหน้ากลุ่มเพื่อน ให้ใช้การเจรจาส่วนตัวเพื่อวิเคราะห์สาเหตุรากเหง้า (Root Cause)</span>
                  </div>
                  <div className="flex items-start gap-2">
                    <span className="text-rose-500 font-bold">▶</span>
                    <span><strong>การจัดกิจกรรมทดแทน (Alternative Activities):</strong> เบี่ยงเบนความสนใจจากพฤติกรรมเสี่ยง (เช่น ติดโซเชียล/หนีเรียน) มาเป็นการมอบหมายภารกิจพิเศษที่นักเรียนถนัด เช่น กิจกรรมจิตอาสา กีฬา หรือศิลปะ</span>
                  </div>
                </>
              )}
              {desCount === 0 && undCount === 0 && (
                <div className="flex items-start gap-2">
                  <span className="text-slate-400 font-bold">▶</span>
                  <span>ไม่พบพฤติกรรมบ่งชี้ที่ชัดเจน เน้นการสังเกตพฤติกรรมในชั้นเรียนทั่วไปและการสร้างสัมพันธภาพที่ดี</span>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="flex justify-end pt-2 border-t">
          <button 
            onClick={onSummaryClose}
            className="px-6 py-3 bg-teal-500 hover:bg-teal-600 text-white font-bold rounded-2xl shadow-md transition-all text-sm"
          >
            รับทราบและปิดหน้ารายงาน
          </button>
        </div>
      </div>
    </div>
  );
}
// ==========================================
// ADMIN DASHBOARD
// ==========================================
function AdminDashboard({ users, st5Data, behaviorData, profile, triggerAlert, triggerConfirm, triggerDownloadConsentPdf }) {
  const [selectedUserId, setSelectedUserId] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  
  // กรองผู้ใช้งานในสังกัด และจัดเรียงตามชื่อ ก-ฮ
  const students = users
    .filter(u => ['student', 'community', 'teacher'].includes(u.accountType) && u.affiliation === profile.affiliation)
    .sort((a, b) => a.name.localeCompare(b.name, 'th'));

  // ค้นหา
  const filteredStudents = students.filter(u => 
    u.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
    (u.id && u.id.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const selectedUser = users.find(u => u.id === selectedUserId);

  return (
    <div className="flex flex-col lg:flex-row gap-6 lg:h-[calc(100vh-160px)]">
      {/* 1. Sidebar แสดงรายชื่อ */}
      <div className={`w-full lg:w-[400px] flex-shrink-0 flex flex-col gap-4 ${selectedUser ? 'hidden lg:flex' : 'flex'}`}>
        <div className="bg-white p-5 rounded-[2rem] shadow-sm border border-slate-100 shrink-0">
          <h2 className="text-xl font-black text-slate-800 flex items-center gap-2 mb-3"><ClipboardList className="text-purple-400"/> รายชื่อในความดูแล</h2>
          <div className="flex flex-col gap-3">
             <div className="inline-flex items-center gap-2 bg-purple-50 px-3 py-1.5 rounded-full border border-purple-100 self-start">
               <span className="text-[10px] font-bold text-purple-400">สังกัด</span>
               <span className="text-xs font-semibold text-purple-700">{profile.affiliation}</span>
             </div>
             
             {/* Filter Input */}
             <div className="relative mt-2">
                <input 
                  type="text" 
                  placeholder="ค้นหารายชื่อ หรือ ID..." 
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-2xl text-sm focus:ring-4 focus:ring-purple-500/20 focus:border-purple-400 outline-none transition-all font-medium text-slate-700"
                />
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
             </div>
          </div>
        </div>

        {/* List of Users */}
        <div className="flex-1 overflow-y-auto hide-scrollbar space-y-3 pb-6">
          {filteredStudents.map(student => {
            const st5Count = st5Data.filter(d => d.uid === student.id || d.userId === student.id).length;
            const behCount = behaviorData.filter(d => d.targetUid === student.id).length;
            const isSelected = selectedUserId === student.id;

            return (
              <div key={student.id} onClick={() => setSelectedUserId(student.id)} 
                   className={`p-4 rounded-[2rem] shadow-sm border flex justify-between items-center hover:shadow-md transition-all cursor-pointer group transform hover:-translate-y-0.5 ${isSelected ? 'bg-purple-50 border-purple-200 ring-2 ring-purple-400/20' : 'bg-white border-slate-100 hover:border-purple-200'}`}>
                <div className="flex items-center gap-4 overflow-hidden">
                  <div className={`w-12 h-12 shrink-0 rounded-full flex items-center justify-center font-black text-lg shadow-inner border border-white transition-colors ${isSelected ? 'bg-purple-500 text-white' : 'bg-gradient-to-br from-purple-100 to-pink-100 text-purple-500'}`}>
                    {student.name.charAt(0)}
                  </div>
                  <div className="min-w-0">
                    <p className={`font-bold truncate text-sm transition ${isSelected ? 'text-purple-700' : 'text-slate-700 group-hover:text-purple-600'}`}>{student.name}</p>
                    <div className="flex items-center gap-1.5 mt-1.5 flex-wrap">
                      <span className="text-[9px] font-bold bg-slate-100 text-slate-500 px-1.5 py-0.5 rounded-md">
                        {student.accountType === 'student' ? 'นักเรียน' : student.accountType === 'teacher' ? 'ครู' : 'ชุมชน'}
                      </span>
                      {st5Count > 0 && <span className="text-[9px] font-bold bg-teal-50 text-teal-600 px-1.5 py-0.5 rounded-md border border-teal-100">ST-5: {st5Count}</span>}
                      {behCount > 0 && <span className="text-[9px] font-bold bg-orange-50 text-orange-600 px-1.5 py-0.5 rounded-md border border-orange-100">พฤติกรรม: {behCount}</span>}
                    </div>
                  </div>
                </div>
                <div className={`w-8 h-8 shrink-0 rounded-full flex items-center justify-center transition-all shadow-sm ${isSelected ? 'bg-purple-500 text-white' : 'bg-slate-50 text-slate-300 group-hover:bg-purple-400 group-hover:text-white'}`}>
                  <ChevronRight size={18} strokeWidth={3}/>
                </div>
              </div>
            );
          })}
          {filteredStudents.length === 0 && (
            <div className="bg-white p-8 rounded-[2rem] text-center border-2 border-dashed border-slate-200">
              <Users className="mx-auto text-slate-300 mb-3" size={36} />
              <p className="text-slate-500 font-medium text-sm">ไม่พบรายชื่อที่ค้นหา</p>
            </div>
          )}
        </div>
      </div>

      {/* 2. Main Content Area */}
      <div className={`w-full lg:flex-1 overflow-y-auto hide-scrollbar bg-slate-50/50 rounded-[2.5rem] border border-slate-100 relative ${!selectedUser ? 'hidden lg:flex items-center justify-center' : 'block'}`}>
        {selectedUser ? (
          <div className="p-4 md:p-6 lg:p-8 min-h-full">
            <AdminStudentDetail 
              student={selectedUser} 
              st5History={st5Data.filter(d => d.uid === selectedUser.id || d.userId === selectedUser.id)} 
              behaviorHistory={behaviorData.filter(d => d.targetUid === selectedUser.id)} 
              onBack={() => setSelectedUserId(null)} 
              triggerAlert={triggerAlert} 
              triggerConfirm={triggerConfirm} 
              triggerDownloadConsentPdf={triggerDownloadConsentPdf} 
            />
          </div>
        ) : (
          <div className="text-center p-8">
             <div className="w-24 h-24 bg-white rounded-full flex items-center justify-center mx-auto mb-6 shadow-sm border border-slate-100">
               <UserSquare2 size={48} className="text-slate-300" strokeWidth={1.5} />
             </div>
             <h3 className="text-xl font-black text-slate-700 mb-2">เลือกรายชื่อในความดูแล</h3>
             <p className="text-slate-500 font-medium text-sm max-w-sm mx-auto">คลิกเลือกนักเรียนหรือผู้ใช้งานจากรายชื่อด้านซ้าย เพื่อดูรายงานผลสุขภาพจิตและประวัติพฤติกรรมอย่างละเอียด</p>
          </div>
        )}
      </div>
    </div>
  );
}

function AdminStudentDetail({ student, st5History, behaviorHistory, onBack, triggerAlert, triggerConfirm, triggerDownloadConsentPdf }) {
  const [showBehaviorForm, setShowBehaviorForm] = useState(false);
  const [editingBehavior, setEditingBehavior] = useState(null);
  const [viewingSt5Result, setViewingSt5Result] = useState(null); 
  const [viewingBehaviorResult, setViewingBehaviorResult] = useState(null);
  const [editingUser, setEditingUser] = useState(false);

  const handleSaveUser = async (uid, updatedData) => {
    await updateDoc(doc(db, 'artifacts', appId, 'public', 'data', 'users', uid), updatedData);
    syncToGoogleSheet('EDIT_USER', { uid, ...updatedData });
    setEditingUser(false);
    triggerAlert('อัปเดตข้อมูลผู้ใช้งานสำเร็จ ✦', 'success');
  };

  const handleDeleteUser = () => {
    triggerConfirm(`ลบผู้ใช้ "${student.name}" ออกจากระบบถาวร ยืนยันหรือไม่?`, async () => {
      await deleteDoc(doc(db, 'artifacts', appId, 'public', 'data', 'users', student.id));
      syncToGoogleSheet('DELETE_USER', { uid: student.id });
      triggerAlert('ลบข้อมูลผู้ใช้งานเรียบร้อยแล้วค่ะ', 'success');
      onBack();
    }, 'danger');
  };

  const saveSuggestion = async (docId, text) => {
    await updateDoc(doc(db, 'artifacts', appId, 'public', 'data', 'st5', docId), { suggestion: text });
    triggerAlert('บันทึกคำแนะนำความห่วงใยเรียบร้อยแล้วค่ะ ✦', 'success');
  };

  const deleteBehavior = (behId, timestamp) => {
    triggerConfirm('ยืนยันการลบประวัติประเมินพฤติกรรมนี้ออกจากระบบ?', async () => {
      await deleteDoc(doc(db, 'artifacts', appId, 'public', 'data', 'behaviors', behId));
      syncToGoogleSheet('DELETE_BEHAVIOR', { targetName: student.name, timestamp: timestamp });
      triggerAlert('ลบประวัติพฤติกรรมเรียบร้อยแล้วค่ะ', 'success');
    }, 'danger');
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {editingUser && (
        <EditUserModal 
          user={student} 
          onClose={() => setEditingUser(false)} 
          onSave={handleSaveUser} 
        />
      )}
      <button onClick={onBack} className="lg:hidden text-slate-400 hover:text-purple-600 mb-2 flex items-center gap-2 font-bold transition bg-white px-4 py-2 rounded-full shadow-sm border border-slate-100 w-fit text-sm">
        <ChevronRight className="rotate-180" size={16}/> กลับไปหน้ารายชื่อ
      </button>

      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 bg-white p-6 md:p-8 rounded-[2.5rem] shadow-sm border border-slate-100">
        <div className="flex items-center gap-5">
           <div className="w-20 h-20 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-full flex items-center justify-center text-purple-600 font-black text-3xl shadow-inner border-2 border-white">
              {student.name.charAt(0)}
           </div>
           <div>
             <h2 className="text-2xl md:text-3xl font-black text-slate-800 tracking-tight">{student.name}</h2>
             <div className="flex items-center gap-2 mt-2 flex-wrap">
                <p className="text-slate-500 text-sm font-medium bg-slate-50 px-3 py-1 rounded-lg">ID: {student.id}</p>
                <button onClick={() => setEditingUser(true)} className="text-sky-500 hover:bg-sky-50 px-3 py-1 rounded-lg text-xs font-bold transition">แก้ไขข้อมูล</button>
                <button onClick={handleDeleteUser} className="text-rose-500 hover:text-white hover:bg-rose-500 px-3 py-1 rounded-lg text-xs font-bold transition border border-rose-100 hover:border-rose-500">ลบข้อมูลผู้ใช้</button>
             </div>
           </div>
        </div>
                <div className="flex flex-col md:flex-row gap-2 w-full md:w-auto">
          <button onClick={() => triggerDownloadConsentPdf(student)} className="bg-purple-100 text-purple-700 px-6 py-4 rounded-2xl font-bold hover:bg-purple-200 shadow-sm transition w-full md:w-auto text-sm flex items-center justify-center gap-2">
            <Download size={18} /> โหลด Consent Form
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
        </div>
      </div>

      {/* POPUP MODAL: รายละเอียดวิชาการ ST-5 */}
      {viewingSt5Result && (
        <ST5ResultModal result={viewingSt5Result} isTeacherView={true} onSummaryClose={() => setViewingSt5Result(null)} />
      )}

      {/* POPUP MODAL: แผนพัฒนาพฤติกรรมย้อนหลัง */}
      {viewingBehaviorResult && (
        <BehaviorResultSummary selections={viewingBehaviorResult} onSummaryClose={() => setViewingBehaviorResult(null)} />
      )}

      {showBehaviorForm && (
        <BehaviorForm 
          targetUser={student} 
          initialData={editingBehavior}
          st5History={st5History}
          behaviorHistory={behaviorHistory}
          triggerAlert={triggerAlert}
          onDone={() => { 
            setShowBehaviorForm(false); 
            setEditingBehavior(null);
            triggerAlert(editingBehavior ? 'อัปเดตผลการประเมินพฤติกรรมเรียบร้อย' : 'บันทึกผลการประเมินพฤติกรรมลงระบบเรียบร้อย', 'success'); 
          }} 
        />
      )}

      <div className="grid lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 md:p-8 rounded-[2.5rem] shadow-sm border border-slate-100">
          <h3 className="font-black text-lg mb-6 text-slate-800 flex items-center gap-2"><HeartPulse className="text-pink-400"/> ข้อมูลสุขภาพจิต (ST-5)</h3>
          <div className="space-y-4">
            {st5History.map((item, idx) => {
              const status = calculateST5(item.score);
              return (
                <div key={item.id} className="p-5 md:p-6 border border-slate-100 rounded-[2rem] bg-slate-50/50 space-y-4">
                  <div className="flex flex-wrap justify-between items-center gap-3">
                    <span className="text-sm font-medium text-slate-500 bg-white px-3 py-1 rounded-full border border-slate-200 shadow-sm">
                      <span className="font-bold text-sky-500 mr-2">ครั้งที่ {st5History.length - idx}</span>
                      {new Date(item.timestamp).toLocaleDateString('th-TH')}
                    </span>
                    <div className="flex items-center gap-2">
                      <button onClick={() => setViewingSt5Result({ score: item.score, ...status })} className="text-xs bg-white text-purple-600 px-3 py-1 border border-purple-200 rounded-full hover:bg-purple-50 transition font-bold shadow-sm">
                        ดูแนวทางวิชาการ
                      </button>
                      <span className={`px-4 py-1.5 rounded-full text-xs font-bold border shadow-sm ${status.color}`}>
                        {item.level || status.level} ({item.score} แต้ม)
                      </span>
                    </div>
                  </div>
                  <textarea 
                    className="w-full p-4 text-sm border border-slate-200 rounded-2xl outline-none focus:ring-4 focus:ring-purple-500/20 focus:border-purple-400 focus:bg-white transition bg-slate-100/50 text-slate-700 resize-none"
                    placeholder="ฝากข้อความให้กำลังใจ หรือ ข้อเสนอแนะ (พิมพ์แล้วระบบบันทึกให้อัตโนมัติ)..."
                    defaultValue={item.suggestion}
                    onBlur={(e) => { if(e.target.value !== item.suggestion) saveSuggestion(item.id, e.target.value); }}
                    rows="2"
                  />
                </div>
              );
            })}
            {st5History.length === 0 && <p className="text-sm text-slate-400 text-center py-10">ยังไม่มีข้อมูลการทำแบบประเมิน</p>}
          </div>
        </div>

        <div className="bg-white p-6 md:p-8 rounded-[2.5rem] shadow-sm border border-slate-100">
          <h3 className="font-black text-lg mb-6 text-slate-800 flex items-center gap-2"><Star className="text-amber-400"/> บันทึกพฤติกรรม</h3>
          <div className="space-y-4">
            {behaviorHistory.map((item, idx) => {
              const desItems = item.selections?.desirable || [];
              const undItems = item.selections?.undesirable || [];
              return (
                <div key={item.id} className="p-5 md:p-6 border border-slate-100 rounded-[2rem] bg-white shadow-sm hover:shadow-md transition space-y-4">
                  <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center border-b pb-3 gap-3">
                     <div className="flex flex-col gap-1">
                       <span className="text-sm font-medium text-slate-500 bg-slate-50 px-3 py-1.5 rounded-full border border-slate-200">
                          <span className="font-bold text-purple-500 mr-2">ครั้งที่ {behaviorHistory.length - idx}</span>
                          {new Date(item.timestamp).toLocaleString('th-TH')}
                        </span>
                        {item.st5RoundId && (
                          <span className="text-xs font-bold text-slate-400 pl-2">
                             📌 อ้างอิง: ST-5 ครั้งที่ {
                               st5History.findIndex(s => s.id === item.st5RoundId) !== -1 
                                 ? st5History.length - st5History.findIndex(s => s.id === item.st5RoundId)
                                 : '?'
                             }
                          </span>
                        )}
                     </div>
                      
                      <div className="flex items-center gap-2 w-full sm:w-auto overflow-x-auto pb-1 sm:pb-0">
                        <button onClick={() => setViewingBehaviorResult(item.selections)} className="text-[11px] bg-teal-50 text-teal-700 px-3 py-1.5 border border-teal-200 rounded-full hover:bg-teal-100 transition font-bold shadow-sm whitespace-nowrap">
                          แผนพัฒนา
                        </button>
                        <button onClick={() => { setEditingBehavior(item); setShowBehaviorForm(true); }} className="text-[11px] bg-sky-50 text-sky-600 px-3 py-1.5 border border-sky-200 rounded-full hover:bg-sky-100 transition font-bold shadow-sm">
                          แก้ไข
                        </button>
                        <button onClick={() => deleteBehavior(item.id, item.timestamp)} className="text-[11px] bg-rose-50 text-rose-600 px-3 py-1.5 border border-rose-200 rounded-full hover:bg-rose-100 transition font-bold shadow-sm">
                          ลบ
                        </button>
                      </div>
                  </div>
                  <div className="space-y-3">
                    {desItems.length > 0 && (
                      <div className="bg-teal-50/30 p-3 rounded-xl border border-teal-100/50">
                        <p className="text-[10px] font-bold text-teal-600 mb-1.5 uppercase tracking-wide">จุดเด่น / พฤติกรรมพึงประสงค์</p>
                        <ul className="text-xs space-y-1">
                          {desItems.map((k) => <li key={k} className="flex items-center gap-2 text-slate-700 font-medium"><CheckCircle2 size={14} className="text-teal-500 shrink-0"/> <span>{k}</span></li>)}
                        </ul>
                      </div>
                    )}
                    {undItems.length > 0 && (
                      <div className="bg-rose-50/30 p-3 rounded-xl border border-rose-100/50">
                        <p className="text-[10px] font-bold text-rose-600 mb-1.5 uppercase tracking-wide">สิ่งที่ควรเฝ้าระวัง</p>
                        <ul className="text-xs space-y-1">
                          {undItems.map((k) => <li key={k} className="flex items-center gap-2 text-slate-700 font-medium"><AlertCircle size={14} className="text-rose-400 shrink-0"/> <span>{k}</span></li>)}
                        </ul>
                      </div>
                    )}
                    {desItems.length === 0 && undItems.length === 0 && <p className="text-sm text-slate-400 italic px-2">ไม่ได้ระบุพฤติกรรมในรอบนี้</p>}
                  </div>
                </div>
              );
            })}
             {behaviorHistory.length === 0 && <p className="text-sm text-slate-400 text-center py-10">ยังไม่มีประวัติบันทึกพฤติกรรม</p>}
          </div>
        </div>
      </div>
    </div>
  );
}

// ==========================================
// SUPERADMIN DASHBOARD
// ==========================================
function SuperAdminDashboard({ users, st5Data, behaviorData, profile, triggerAlert, triggerConfirm, triggerDownloadConsentPdf }) {
  const [editingUser, setEditingUser] = useState(null);
  
  const displayUsers = profile.id === 'rung' ? users : users.filter(u => Array.isArray(profile.affiliation) ? profile.affiliation.includes(u.affiliation) : u.affiliation === profile.affiliation);
  const pendingAdmins = displayUsers.filter(u => u.role === 'admin' && u.status === 'pending');

  const approveAdmin = async (uid) => {
    await updateDoc(doc(db, 'artifacts', appId, 'public', 'data', 'users', uid), { status: 'approved' });
    syncToGoogleSheet('UPDATE_STATUS', { uid, status: 'approved' });
    triggerAlert('อนุมัติสิทธิ์การดูแลระบบให้คุณครูท่านนี้สำเร็จแล้วค่ะ ✦', 'success');
  };

  const toggleStatus = (uid, currentStatus, name) => {
    const newStatus = currentStatus === 'suspended' ? 'approved' : 'suspended';
    const actionName = currentStatus === 'suspended' ? 'ปลดระงับ' : 'ระงับ';
    
    triggerConfirm(`ต้องการ${actionName}สิทธิ์การใช้งานของ "${name}" ยืนยันหรือไม่?`, async () => {
      await updateDoc(doc(db, 'artifacts', appId, 'public', 'data', 'users', uid), { status: newStatus });
      syncToGoogleSheet('UPDATE_STATUS', { uid, status: newStatus });
      triggerAlert(`${actionName}สิทธิ์การใช้งานสำเร็จเรียบร้อย`, 'success');
    });
  };

  const handleSaveEdit = async (uid, updatedData) => {
    await updateDoc(doc(db, 'artifacts', appId, 'public', 'data', 'users', uid), updatedData);
    syncToGoogleSheet('EDIT_USER', { uid, ...updatedData });
    setEditingUser(null);
    triggerAlert('อัปเดตข้อมูลผู้ใช้งานและรหัสผ่านสำเร็จ ✦', 'success');
  };

  const deleteUser = (uid, name) => {
    triggerConfirm(`ลบผู้ใช้ "${name}" ออกจากระบบถาวร ยืนยันหรือไม่?`, async () => {
      await deleteDoc(doc(db, 'artifacts', appId, 'public', 'data', 'users', uid));
      syncToGoogleSheet('DELETE_USER', { uid });
      triggerAlert('ลบข้อมูลผู้ใช้งานเรียบร้อยแล้วค่ะ', 'success');
    }, 'danger');
  };

  return (
    <div className="space-y-6 md:space-y-8">
      {/* 🟢 Popup Modal สำหรับแก้ไขข้อมูลผู้ใช้งาน */}
      {editingUser && (
        <EditUserModal 
          user={editingUser} 
          onClose={() => setEditingUser(null)} 
          onSave={handleSaveEdit} 
        />
      )}

      <div className="bg-white p-6 md:p-8 rounded-[2.5rem] shadow-sm border border-slate-100">
        <h3 className="font-black text-xl mb-6 text-orange-500 flex items-center gap-2"><Clock size={24}/> คำขออนุมัติสิทธิ์แอดมิน</h3>
        {pendingAdmins.length === 0 ? (
          <p className="text-sm text-slate-400 bg-slate-50 p-6 rounded-2xl text-center border border-dashed border-slate-200">เรียบร้อยดี ไม่มีรายการค้างอนุมัติค่ะ</p>
        ) : (
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {pendingAdmins.map(admin => (
              <li key={admin.id} className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 p-5 border border-orange-100 rounded-2xl bg-orange-50/50">
                <div>
                  <span className="font-bold text-slate-800 text-base">{admin.name}</span>
                  <span className="text-xs font-medium text-orange-600 block mt-1 bg-white px-2 py-1 rounded-md inline-block shadow-sm">{admin.affiliation}</span>
                </div>
                <button onClick={() => approveAdmin(admin.id)} className="bg-orange-500 text-white px-5 py-2.5 text-sm font-bold rounded-xl hover:bg-orange-600 shadow-md transition w-full sm:w-auto">
                  อนุมัติ
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="bg-white p-6 md:p-8 rounded-[2.5rem] shadow-sm border border-slate-100">
        <h3 className="font-black text-xl mb-6 text-slate-800">จัดการผู้ใช้งานทั้งหมดในระบบ</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm min-w-[800px]">
            <thead>
              <tr className="border-b-2 border-slate-100">
                <th className="p-4 font-bold text-slate-400 uppercase tracking-wider text-xs">ผู้ใช้</th>
                <th className="p-4 font-bold text-slate-400 uppercase tracking-wider text-xs">สังกัด</th>
                <th className="p-4 font-bold text-slate-400 uppercase tracking-wider text-xs text-center">สถานะ</th>
                <th className="p-4 font-bold text-slate-400 uppercase tracking-wider text-xs text-right">จัดการข้อมูล (Admin / User)</th>
              </tr>
            </thead>
            <tbody>
              {displayUsers.map(u => (
                <tr key={u.id} className="border-b border-slate-50 hover:bg-slate-50 transition">
                  <td className="p-4">
                    <p className="font-bold text-slate-700">{u.name}</p>
                    <p className="text-[10px] text-slate-400 font-mono mt-0.5">@{u.id}</p>
                    <span className="text-[10px] font-bold text-purple-500 bg-purple-50 px-2 py-0.5 rounded-md mt-1 inline-block">
                      {u.accountType === 'student' ? 'นักเรียน' : u.accountType === 'teacher' ? 'ครู' : u.accountType === 'community' ? 'ชุมชน' : u.accountType === 'admin' ? 'Admin' : 'Superadmin'}
                    </span>
                  </td>
                  <td className="p-4 text-xs text-slate-500 font-medium">{displayAffiliation(u.affiliation) || '-'}</td>
                  <td className="p-4 text-center">
                     <span className={`px-3 py-1 rounded-md text-[10px] font-bold uppercase tracking-wide border ${
                        u.status === 'approved' ? 'bg-teal-50 text-teal-600 border-teal-100' : 
                        u.status === 'suspended' ? 'bg-rose-50 text-rose-600 border-rose-100' : 
                        'bg-orange-50 text-orange-600 border-orange-100'
                     }`}>
                      {u.status === 'approved' ? 'อนุมัติแล้ว' : u.status === 'suspended' ? 'ระงับสิทธิ์' : 'รอตรวจสอบ'}
                    </span>
                  </td>
                  <td className="p-4 text-right">
                    {(u.role === 'user' || u.role === 'admin') ? (
                      <div className="flex items-center justify-end gap-2">
                        <button onClick={() => triggerDownloadConsentPdf(u)} className="text-purple-500 hover:bg-purple-50 px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1">
                           <Download size={12}/> PDF
                        </button>
                        <button onClick={() => toggleStatus(u.id, u.status, u.name)} className={`${u.status === 'suspended' ? 'text-emerald-500 hover:bg-emerald-50' : 'text-amber-500 hover:bg-amber-50'} px-3 py-1.5 rounded-lg text-xs font-bold transition`}>
                          {u.status === 'suspended' ? 'ปลดระงับ' : 'ระงับ'}
                        </button>
                        <button onClick={() => setEditingUser(u)} className="text-sky-500 hover:bg-sky-50 px-3 py-1.5 rounded-lg text-xs font-bold transition">แก้ไข</button>
                        <button onClick={() => deleteUser(u.id, u.name)} className="text-rose-400 hover:text-white hover:bg-rose-500 px-3 py-1.5 rounded-lg text-xs font-bold transition">ลบ</button>
                      </div>
                    ) : null}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// 🟢 Component ย่อยสำหรับการแก้ไขข้อมูล User (แสดงเป็น Popup)
function EditUserModal({ user, onClose, onSave }) {
  const [formData, setFormData] = useState({
    name: user.name || '',
    accountType: user.accountType || 'student',
    affiliation: user.affiliation || '',
    status: user.status || 'approved',
    password: user.password || ''
  });

  const handleSave = () => {
    const role = getRoleFromAccountType(formData.accountType);
    onSave(user.id, { ...formData, role });
  };

  const inputClass = "w-full p-3.5 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-purple-500/20 focus:border-purple-400 outline-none bg-slate-50 hover:bg-white transition-all text-sm font-medium text-slate-700";
  const labelClass = "block text-xs font-bold text-slate-500 mb-1.5 pl-1";

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="w-full max-w-md bg-white p-6 md:p-8 rounded-[2.5rem] shadow-2xl border border-slate-100 space-y-4 animate-in zoom-in-95 duration-300">
        <div className="flex justify-between items-center border-b pb-4 mb-2">
          <h4 className="text-lg font-black text-slate-800">✏️ แก้ไขข้อมูลผู้ใช้งาน</h4>
          <button onClick={onClose} className="text-slate-400 hover:text-rose-500 hover:bg-rose-50 p-1.5 rounded-full transition"><XCircle size={24} /></button>
        </div>
        
        <div className="space-y-4">
          <div>
            <label className={labelClass}>ชื่อ-นามสกุล</label>
            <input type="text" className={inputClass} value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} />
          </div>
          <div>
            <label className={labelClass}>รหัสผ่าน</label>
            <input type="text" className={inputClass} value={formData.password} onChange={e => setFormData({...formData, password: e.target.value})} placeholder="กำหนดรหัสผ่านใหม่" />
          </div>
          <div>
            <label className={labelClass}>ประเภทบัญชี</label>
            <select className={inputClass} value={formData.accountType} onChange={e => {
              const newType = e.target.value;
              const newOpts = getAffiliationOptions(newType);
              setFormData({...formData, accountType: newType, affiliation: newOpts[0] || ''});
            }}>
              <option value="student">นักเรียน</option>
              <option value="community">คนในชุมชน</option>
              <option value="teacher">คุณครู</option>
              <option value="admin">ครู/ผู้รับผิดชอบ (Admin)</option>
            </select>
          </div>
          <div>
            <label className={labelClass}>สังกัด (ข้อมูลตามประเภทบัญชี)</label>
            <select className={inputClass} value={formData.affiliation} onChange={e => setFormData({...formData, affiliation: e.target.value})}>
              {getAffiliationOptions(formData.accountType).map((opt, idx) => <option key={idx} value={opt}>{opt}</option>)}
            </select>
          </div>
          <div>
            <label className={labelClass}>สถานะการเข้าใช้งาน</label>
            <select className={inputClass} value={formData.status} onChange={e => setFormData({...formData, status: e.target.value})}>
              <option value="approved">✅ อนุมัติแล้ว (ใช้งานได้ปกติ)</option>
              <option value="pending">⏳ รอตรวจสอบ</option>
              <option value="suspended">🚫 ระงับสิทธิ์ (ห้ามเข้าใช้)</option>
            </select>
          </div>
        </div>

        <div className="flex gap-3 mt-6 pt-5 border-t border-slate-100">
          <button onClick={onClose} className="flex-1 py-3.5 bg-slate-100 text-slate-500 rounded-2xl font-bold hover:bg-slate-200 transition text-sm">ยกเลิก</button>
          <button onClick={handleSave} className="flex-1 py-3.5 bg-purple-500 text-white rounded-2xl font-bold hover:bg-purple-600 transition shadow-lg shadow-purple-100 text-sm">บันทึกการแก้ไข</button>
        </div>
      </div>
    </div>
  );
}

// ==========================================
// SYNC DASHBOARD (ONLY FOR RUNG)
// ==========================================
function SyncDashboard({ triggerAlert, triggerConfirm, st5Data, behaviorData }) {
  const [isSyncing, setIsSyncing] = useState(false);
  const [logs, setLogs] = useState([]);

  const addLog = (message, type = 'info') => {
    const time = new Date().toLocaleTimeString('th-TH');
    setLogs(prev => [{ time, message, type }, ...prev]);
  };

  const handleSync = () => {
    triggerConfirm('ยืนยันการดึงข้อมูลจาก Google Sheets กลับเข้าระบบฐานข้อมูลหลัก?\n\n(ระบบจะอ่านข้อมูลจากชีตและนำข้อมูลที่ขาดหายไปมาเพิ่มอัตโนมัติ)', async () => {
      setIsSyncing(true);
      addLog('เริ่มต้นการเชื่อมต่อกับ Google Sheets API...', 'info');

      try {
        addLog('กำลังส่งคำร้องขอ (GET) ไปยัง Google Web App URL...', 'info');
        
        const response = await fetch(GAS_URL + "?action=sync", { 
           method: 'GET'
        });
        
        if(!response.ok) throw new Error(`HTTP Error: ${response.status}`);
        
        const text = await response.text();
        let result;
        try {
          result = JSON.parse(text);
        } catch (e) {
          console.error("Response is not JSON:", text);
          throw new Error('ข้อมูลตอบกลับไม่ใช่รูปแบบ JSON (โปรดตรวจสอบว่าได้อัปเดตโค้ด doGet ใน Apps Script และกด Deploy เป็น "เวอร์ชันใหม่" แล้วหรือไม่)');
        }
        
        addLog('เชื่อมต่อสำเร็จ ดาวน์โหลดข้อมูลจากชีตเรียบร้อย', 'success');

        // Process Users
        if (result.users && result.users.length > 0) {
           addLog(`พบข้อมูลผู้ใช้งาน ${result.users.length} รายการ กำลังตรวจสอบและอัปเดต...`, 'info');
           let addedUsers = 0;
           let updatedUsers = 0;
           for(let u of result.users) {
              if(!u.username) continue;
              // Prevent duplicate by forcing lowercase and trim on username which is the primary ID
              const uid = String(u.username).toLowerCase().trim();
              const docRef = doc(db, 'artifacts', appId, 'public', 'data', 'users', uid);
              const snap = await getDoc(docRef);
              
              let accType = 'student';
              if(u.accountType === 'ครู') accType = 'teacher';
              else if(u.accountType === 'ชุมชน') accType = 'community';
              else if(u.accountType === 'แอดมิน' || u.accountType === 'Admin' || String(u.role).toLowerCase() === 'admin') accType = 'admin';
              else if(u.accountType === 'ซุปเปอร์แอดมิน' || String(u.role).toLowerCase() === 'superadmin') accType = 'superadmin';

              const userData = {
                 username: uid,
                 name: u.name || '',
                 role: u.role ? u.role.toLowerCase() : 'user',
                 accountType: accType,
                 affiliation: u.affiliation || '',
                 status: u.status || 'approved',
                 password: u.password || '123', // ดึงรหัสผ่านจาก Sheet ถ้าไม่มีใช้ 123
                 createdAt: parseSheetDate(u.createdAt)
              };

              if(!snap.exists()) {
                 await setDoc(docRef, userData);
                 addedUsers++;
              } else {
                 // Update missing or changed fields from Sheet, including password
                 await updateDoc(docRef, {
                    name: userData.name,
                    accountType: userData.accountType,
                    affiliation: userData.affiliation,
                    role: userData.role,
                    status: userData.status,
                    password: userData.password
                 });
                 updatedUsers++;
              }
           }
           addLog(`ดึงข้อมูลผู้ใช้เพิ่มใหม่ ${addedUsers} รายการ, อัปเดตข้อมูลเดิม ${updatedUsers} รายการ`, 'success');
        }

        // Fetch all users mapping for references
        const usersSnap = await getDocs(collection(db, 'artifacts', appId, 'public', 'data', 'users'));
        const nameToUid = {};
        usersSnap.forEach(d => { nameToUid[d.data().name] = d.id });

        // Process ST5
        if (result.st5 && result.st5.length > 0) {
           addLog(`พบข้อมูลคัดกรอง ST-5 จำนวน ${result.st5.length} รายการ กำลังตรวจสอบและซิงก์...`, 'info');
           let addedSt5 = 0;
           for(let s of result.st5) {
               if(!s.timestamp || !s.userName) continue;
               const ts = parseSheetDate(s.timestamp);
               
               // ตรวจสอบข้อมูลซ้ำซ้อน
               const exist = st5Data.find(d => d.userName === s.userName && Math.abs(d.timestamp - ts) < 120000);
               if(!exist) {
                   const uid = nameToUid[s.userName] || `imported_${Date.now().toString().slice(-6)}`;
                   await addDoc(collection(db, 'artifacts', appId, 'public', 'data', 'st5'), {
                       uid: uid,
                       userName: s.userName,
                       answers: [0,0,0,0,0], // ไม่ได้เก็บรายข้อไว้ในชีต จำลองเป็น 0
                       score: Number(s.score) || 0,
                       level: s.level || '',
                       timestamp: ts,
                       suggestion: ''
                   });
                   addedSt5++;
               }
           }
           if(addedSt5 > 0) addLog(`ดึงข้อมูลประเมิน ST-5 ใหม่เพิ่มสำเร็จ ${addedSt5} รายการ`, 'success');
           else addLog(`ข้อมูล ST-5 เป็นปัจจุบันแล้ว`, 'success');
        }

        // Process Behaviors
        if (result.behaviors && result.behaviors.length > 0) {
           addLog(`พบข้อมูลพฤติกรรม จำนวน ${result.behaviors.length} รายการ กำลังตรวจสอบและซิงก์...`, 'info');
           let addedBeh = 0;
           for(let b of result.behaviors) {
               if(!b.timestamp || !b.targetName) continue;
               const ts = parseSheetDate(b.timestamp);
               
               const exist = behaviorData.find(d => d.targetName === b.targetName && Math.abs(d.timestamp - ts) < 120000);
               if(!exist) {
                   const uid = nameToUid[b.targetName] || `imported_${Date.now().toString().slice(-6)}`;
                   const des = b.desirable ? String(b.desirable).split(',').map(x=>x.trim()).filter(x=>x) : [];
                   const und = b.undesirable ? String(b.undesirable).split(',').map(x=>x.trim()).filter(x=>x) : [];
                   
                   await addDoc(collection(db, 'artifacts', appId, 'public', 'data', 'behaviors'), {
                       targetUid: uid,
                       targetName: b.targetName,
                       selections: { desirable: des, undesirable: und },
                       timestamp: ts
                   });
                   addedBeh++;
               }
           }
           if(addedBeh > 0) addLog(`ดึงข้อมูลพฤติกรรมใหม่เพิ่มสำเร็จ ${addedBeh} รายการ`, 'success');
           else addLog(`ข้อมูลพฤติกรรมเป็นปัจจุบันแล้ว`, 'success');
        }

        addLog('✨ อัปเดตข้อมูลทั้งหมดจาก Sheet เข้าสู่ฐานข้อมูลระบบหลักเรียบร้อยแล้ว!', 'success');
        triggerAlert('ดึงข้อมูลจาก Google Sheets ลงฐานข้อมูลสำเร็จแล้วค่ะ ✦', 'success');
        
      } catch (error) {
        console.error(error);
        addLog(`เกิดข้อผิดพลาด: ${error.message}`, 'error');
        triggerAlert('การซิงก์ข้อมูลล้มเหลว โปรดตรวจสอบ Logs', 'error');
      } finally {
        setIsSyncing(false);
      }
    });
  };

  return (
    <div className="space-y-6 md:space-y-8 animate-in fade-in">
      <div className="bg-white p-6 md:p-8 rounded-[2.5rem] shadow-sm border border-slate-100 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div>
          <h2 className="text-2xl md:text-3xl font-black text-slate-800 flex items-center gap-3">
            <Database className="text-indigo-500" size={32}/> ระบบซิงโครไนซ์ข้อมูล
          </h2>
          <p className="text-slate-500 font-medium mt-2 leading-relaxed">
            ดึงข้อมูลสำรองจาก Google Sheets กลับมายังฐานข้อมูลระบบ <br className="hidden md:block"/>
            <span className="text-rose-600 text-[11px] bg-rose-50 px-3 py-1 rounded-md border border-rose-100 mt-2 inline-block font-bold">
              สิทธิ์พิเศษเฉพาะผู้ดูแลระบบ: Rung (Superadmin)
            </span>
          </p>
        </div>
        <button 
          onClick={handleSync}
          disabled={isSyncing}
          className="w-full md:w-auto bg-gradient-to-r from-indigo-500 to-purple-500 text-white px-8 py-4 rounded-2xl font-bold shadow-lg shadow-indigo-200 hover:opacity-90 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {isSyncing ? <RefreshCw className="animate-spin" size={20} /> : <Download size={20} />}
          {isSyncing ? 'กำลังซิงก์ข้อมูล...' : 'เริ่มดึงข้อมูล (Sync)'}
        </button>
      </div>

      <div className="bg-slate-900 p-6 rounded-[2rem] shadow-inner border border-slate-800 min-h-[350px] flex flex-col">
        <h3 className="font-bold text-slate-300 text-sm mb-4 flex items-center gap-2 border-b border-slate-700 pb-4">
          <Terminal size={18} className="text-emerald-400"/> Terminal Logs (สถานะการซิงก์)
        </h3>
        <div className="flex-1 overflow-y-auto space-y-2.5 max-h-96 custom-scrollbar pr-2 font-mono text-xs">
          {logs.length === 0 ? (
            <p className="text-slate-600 italic">... รอการกดปุ่มเริ่มต้นคำสั่งซิงก์ข้อมูล ...</p>
          ) : (
            logs.map((log, idx) => (
              <div key={idx} className="flex items-start gap-3">
                <span className="text-slate-500 shrink-0">[{log.time}]</span>
                <span className={
                  log.type === 'error' ? 'text-rose-400' :
                  log.type === 'success' ? 'text-emerald-400' : 'text-sky-300'
                }>
                  {log.message}
                </span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
// ==========================================
// EXECUTIVE ANALYTICS DASHBOARD - EXPANDED ACADEMIC LEVEL
// ==========================================
function ExecutiveAnalyticsDashboard({ users, st5Data, behaviorData, profile }) {
  const [selectedAffiliation, setSelectedAffiliation] = useState(profile.role === 'superadmin' ? 'all' : profile.affiliation);
  const [selectedUserFilter, setSelectedUserFilter] = useState('all');
  const [subTab, setSubTab] = useState('overview'); // overview, mental, behavior, policy
  const [selectedStudentForDetail, setSelectedStudentForDetail] = useState(null);
  const [viewingSt5Result, setViewingSt5Result] = useState(null);
  const [viewingBehaviorResult, setViewingBehaviorResult] = useState(null);

  const baseStudents = users.filter(u => ['student', 'community', 'teacher'].includes(u.accountType) && (profile.role === 'superadmin' || u.affiliation === profile.affiliation));

  const availableAffiliations = profile.role === 'superadmin' 
    ? [...new Set(baseStudents.map(u => u.affiliation).filter(Boolean))] 
    : [profile.affiliation];

  const studentsInAffiliation = selectedAffiliation === 'all'
    ? baseStudents
    : baseStudents.filter(u => u.affiliation === selectedAffiliation);

  const finalStudents = selectedUserFilter === 'all'
    ? studentsInAffiliation
    : studentsInAffiliation.filter(u => u.id === selectedUserFilter);

  const isIndividualMode = selectedUserFilter !== 'all';
  const individualUser = isIndividualMode ? finalStudents[0] : null;

  const handleAffiliationChange = (e) => {
    setSelectedAffiliation(e.target.value);
    setSelectedUserFilter('all');
  };

  const studentIds = new Set(finalStudents.map(u => u.id));
  const relevantSt5 = st5Data.filter(d => studentIds.has(d.uid) || studentIds.has(d.userId));
  const relevantBehaviors = behaviorData.filter(d => studentIds.has(d.targetUid));

  const usersWithSt5 = new Set(relevantSt5.map(d => d.uid || d.userId)).size;
  const coverageSt5 = finalStudents.length > 0 ? (usersWithSt5 / finalStudents.length) * 100 : 0;

  // Compile datasets for each student
  const aggregatedData = finalStudents.map(user => {
    const uSt5 = relevantSt5.filter(s => s.uid === user.id || s.userId === user.id);
    const latestSt5 = uSt5.length > 0 ? uSt5[0] : null;
    const latestScore = latestSt5 ? latestSt5.score : null;
    const sleepScore = (latestSt5 && latestSt5.answers && latestSt5.answers.length > 0) ? latestSt5.answers[0] : null;

    const uBeh = relevantBehaviors.filter(b => b.targetUid === user.id);
    
    let totalBadBehaviors = 0;
    let totalGoodBehaviors = 0;
    let badCategories = {};
    let goodCategories = {};

    uBeh.forEach(beh => {
      if (beh.selections && beh.selections.undesirable) {
        totalBadBehaviors += beh.selections.undesirable.length;
        beh.selections.undesirable.forEach(item => { badCategories[item] = (badCategories[item] || 0) + 1; });
      }
      if (beh.selections && beh.selections.desirable) {
        totalGoodBehaviors += beh.selections.desirable.length;
        beh.selections.desirable.forEach(item => { goodCategories[item] = (goodCategories[item] || 0) + 1; });
      }
    });

    return { 
      uid: user.id, 
      name: user.name, 
      st5Score: latestScore, 
      sleepScore: sleepScore,
      riskGroup: latestScore !== null ? calculateST5(latestScore).risk : 'N/A', 
      totalBadBehaviors,
      totalGoodBehaviors,
      badCategories,
      goodCategories,
      affiliation: user.affiliation || 'ไม่ระบุสังกัด/สถานที่'
    };
  });

  const validForCorrelation = aggregatedData.filter(d => d.st5Score !== null);
  const totalEvaluated = validForCorrelation.length;

  // --- EXECUTIVE KPIs ---
  const countHighStress = validForCorrelation.filter(d => ['High', 'Severe'].includes(d.riskGroup)).length;
  const pctHighStress = totalEvaluated ? ((countHighStress / totalEvaluated) * 100).toFixed(1) : 0;

  const countBehavior = (itemName, type = 'bad') => {
    let c = 0;
    aggregatedData.forEach(d => {
       if (type === 'bad' && d.badCategories[itemName]) c++;
       if (type === 'good' && d.goodCategories[itemName]) c++;
    });
    return c;
  };

  const usersWithBehaviors = aggregatedData.filter(d => d.totalBadBehaviors > 0 || d.totalGoodBehaviors > 0).length || 1; // prevent div/0
  const pctBullying = ((countBehavior("การใช้ความรุนแรงและรังแกกัน (Bullying)", 'bad') / usersWithBehaviors) * 100).toFixed(1);
  const pctGaming = ((countBehavior("การหมกมุ่นกับสื่อออนไลน์", 'bad') / usersWithBehaviors) * 100).toFixed(1);
  const pctTruancy = ((countBehavior("การหนีเรียน", 'bad') / usersWithBehaviors) * 100).toFixed(1);
  const pctSubstance = ((countBehavior("การใช้สารเสพติด", 'bad') / usersWithBehaviors) * 100).toFixed(1);

  // Well-being Score (0-100) : (Base 100 - Avg Stress Penalty) + (Avg Positive Behavior Bonus) - (Avg Negative Penalty)
  const avgSt5 = validForCorrelation.reduce((acc, val) => acc + val.st5Score, 0) / (totalEvaluated || 1);
  const avgGoodBeh = aggregatedData.reduce((acc, val) => acc + val.totalGoodBehaviors, 0) / (aggregatedData.length || 1);
  const avgBadBeh = aggregatedData.reduce((acc, val) => acc + val.totalBadBehaviors, 0) / (aggregatedData.length || 1);
  let wellbeingScore = 100 - (avgSt5 * 3.33) + (avgGoodBeh * 5) - (avgBadBeh * 8);
  wellbeingScore = Math.max(0, Math.min(100, wellbeingScore));

  // --- RADAR CHART DATA (POSITIVE BEHAVIORS) ---
  const posBehaviorsList = [
    "การใฝ่เรียนรู้", "การคิดวิเคราะห์", "การแก้ปัญหา", 
    "การควบคุมอารมณ์", "ความเห็นอกเห็นใจผู้อื่น", "ความภาคภูมิใจในตนเอง", 
    "ความรับผิดชอบและวินัย", "จิตสาธารณะ", "การดูแลสุขภาพกาย"
  ];
  
  const radarData = posBehaviorsList.map(item => ({
    subject: item.replace('การ', '').replace('ความ', ''), // Shorten labels
    A: countBehavior(item, 'good'),
    fullMark: usersWithBehaviors
  }));

  // --- NEGATIVE BEHAVIORS DATA ---
  const negBehaviorsList = [
    "การใช้ความรุนแรงและรังแกกัน (Bullying)", 
    "การก่อความเดือดร้อนรำคาญ",
    "การใช้สารเสพติด", 
    "การพนัน", 
    "พฤติกรรมทางเพศที่ไม่ปลอดภัย",
    "ภาวะซึมเศร้าและวิตกกังวล",
    "อารมณ์ฉุนเฉียวและก้าวร้าว",
    "การหนีเรียน", 
    "พฤติกรรมถดถอยในการเรียน",
    "การหมกมุ่นกับสื่อออนไลน์"
  ];

  const negativeChartData = negBehaviorsList.map(item => {
    let shortName = item;
    if (item === "การใช้ความรุนแรงและรังแกกัน (Bullying)") shortName = "Bullying";
    else if (item === "การก่อความเดือดร้อนรำคาญ") shortName = "เดือดร้อนรำคาญ";
    else if (item === "การใช้สารเสพติด") shortName = "สารเสพติด";
    else if (item === "การพนัน") shortName = "พนัน";
    else if (item === "พฤติกรรมทางเพศที่ไม่ปลอดภัย") shortName = "พฤติกรรมทางเพศ";
    else if (item === "ภาวะซึมเศร้าและวิตกกังวล") shortName = "ซึมเศร้า/วิตกกังวล";
    else if (item === "อารมณ์ฉุนเฉียวและก้าวร้าว") shortName = "ก้าวร้าว";
    else if (item === "การหนีเรียน") shortName = "หนีเรียน";
    else if (item === "พฤติกรรมถดถอยในการเรียน") shortName = "เรียนถดถอย";
    else if (item === "การหมกมุ่นกับสื่อออนไลน์") shortName = "ติดสื่อออนไลน์";
    
    return {
      name: shortName,
      count: countBehavior(item, 'bad')
    };
  }).sort((a, b) => b.count - a.count);

  const radarMaxPos = Math.max(...radarData.map(d => d.A));
  const radarDomainMax = radarMaxPos === 0 ? 1 : 'dataMax';

  // --- AI INSIGHTS ENGINE ---
  const generateAIInsights = () => {
    let insights = [];
    if (totalEvaluated < 5) return ["ข้อมูลยังไม่เพียงพอสำหรับการวิเคราะห์เชิงลึกด้วย AI (ต้องการข้อมูลอย่างน้อย 5 เคส)"];

    // Insight 1: Sleep vs Stress
    const poorSleepUsers = validForCorrelation.filter(u => u.sleepScore >= 2);
    if (poorSleepUsers.length > 0) {
      const highStressInPoorSleep = poorSleepUsers.filter(u => ['High', 'Severe'].includes(u.riskGroup)).length;
      const ratioPoorSleep = highStressInPoorSleep / poorSleepUsers.length;
      const ratioNormal = countHighStress / totalEvaluated;
      if (ratioPoorSleep > ratioNormal && ratioNormal > 0) {
        const multiplier = (ratioPoorSleep / ratioNormal).toFixed(1);
        insights.push(`นักเรียนที่มีปัญหาการนอนหลับ (ได้คะแนน ST-5 ข้อ 1 ระดับบ่อยครั้งขึ้นไป) มีความเสี่ยงที่จะเกิดภาวะเครียดสูงมากกว่ากลุ่มปกติถึง ${multiplier} เท่า ควรจัดให้มีการคัดกรองภาวะซึมเศร้าร่วมด้วย`);
      } else if (ratioPoorSleep > 0.5) {
        insights.push(`กว่า ${(ratioPoorSleep*100).toFixed(0)}% ของนักเรียนที่มีปัญหาการนอนหลับ มีภาวะเครียดในระดับสูง สะท้อนถึงปัญหาทางสรีรวิทยาที่กระทบต่อจิตใจโดยตรง`);
      }
    }

    // Insight 2: Physical Health vs Gaming/Stress
    const lowHealthUsers = aggregatedData.filter(u => !u.goodCategories["การดูแลสุขภาพกาย"]);
    if (lowHealthUsers.length > 0) {
      const gamingInLowHealth = lowHealthUsers.filter(u => u.badCategories["การหมกมุ่นกับสื่อออนไลน์"]).length;
      const pctGamingLowHealth = (gamingInLowHealth / lowHealthUsers.length) * 100;
      if (Number(pctGamingLowHealth) > Number(pctGaming) * 1.5 && Number(pctGaming) > 0) {
         insights.push(`พบความเชื่อมโยงน่าสนใจ: นักเรียนที่ขาดการดูแลสุขภาพกาย มีโอกาสที่จะมีพฤติกรรมติดเกม/สื่อออนไลน์ สูงถึง ${pctGamingLowHealth.toFixed(0)}% (สูงกว่าค่าเฉลี่ยปกติ)`);
      }
    }

    // Insight 3: Self-esteem vs Bullying
    const lowEsteemUsers = aggregatedData.filter(u => !u.goodCategories["ความภาคภูมิใจในตนเอง"]);
    const highEsteemUsers = aggregatedData.filter(u => u.goodCategories["ความภาคภูมิใจในตนเอง"]);
    
    let bullyLowEsteemRate = 0, bullyHighEsteemRate = 0;
    if (lowEsteemUsers.length > 0) bullyLowEsteemRate = lowEsteemUsers.filter(u => u.badCategories["การใช้ความรุนแรงและรังแกกัน (Bullying)"]).length / lowEsteemUsers.length;
    if (highEsteemUsers.length > 0) bullyHighEsteemRate = highEsteemUsers.filter(u => u.badCategories["การใช้ความรุนแรงและรังแกกัน (Bullying)"]).length / highEsteemUsers.length;

    if (bullyLowEsteemRate > bullyHighEsteemRate + 0.1) {
       insights.push(`ผู้เรียนที่ไม่มีบันทึก 'ความภาคภูมิใจในตนเอง (Self-esteem)' มีแนวโน้มเกี่ยวข้องกับพฤติกรรม Bullying มากกว่ากลุ่มที่เห็นคุณค่าในตนเอง (ชี้ให้เห็นว่าการเสริม Self-esteem คือปัจจัยปกป้องที่สำคัญ)`);
    }

    // Insight 4: Truancy Early Warning
    const truancyUsers = validForCorrelation.filter(u => u.badCategories["การหนีเรียน"]);
    const stressTruancy = truancyUsers.filter(u => ['High', 'Severe'].includes(u.riskGroup)).length;
    if (truancyUsers.length > 0 && stressTruancy / truancyUsers.length > 0.4) {
       insights.push(`Alert: ${(stressTruancy/truancyUsers.length*100).toFixed(0)}% ของกลุ่มเด็กหนีเรียน มีภาวะความเครียดวิกฤตซ่อนอยู่ การลงโทษทางวินัยอาจไม่ใช่วิธีแก้ปัญหา แต่ควรใช้ Psychological First Aid (PFA) แทน`);
    }

    if (insights.length === 0) {
      insights.push("ระดับสุขภาพจิตและพฤติกรรมของประชากรกลุ่มนี้ยังอยู่ในเกณฑ์ที่สอดคล้องกันและควบคุมได้ดี ไม่มีสัญญาณเตือนภัยที่น่ากังวลแบบก้าวกระโดด");
    }

    return insights;
  };

  const aiInsightTexts = useMemo(() => generateAIInsights(), [validForCorrelation.length, aggregatedData.length]);

  const chartDataRisk = [
    { name: 'เครียดน้อย', count: aggregatedData.filter(d => d.riskGroup === 'Low').length, fill: '#5eead4' },
    { name: 'เครียดปานกลาง', count: aggregatedData.filter(d => d.riskGroup === 'Medium').length, fill: '#fcd34d' },
    { name: 'เครียดมาก', count: aggregatedData.filter(d => d.riskGroup === 'High').length, fill: '#fca5a5' },
    { name: 'เครียดมากที่สุด', count: aggregatedData.filter(d => d.riskGroup === 'Severe').length, fill: '#f87171' },
  ];

  const maxRisk = chartDataRisk.reduce((max, current) => current.count > max.count ? current : max, chartDataRisk[0]);
  const totalRisk = chartDataRisk.reduce((sum, current) => sum + current.count, 0);
  const maxRiskPct = totalRisk > 0 ? Math.round((maxRisk.count / totalRisk) * 100) : 0;
  const st5Interpretation = `การแปรผล: ส่วนใหญ่อยู่ในเกณฑ์ "${maxRisk?.name || 'ไม่มีข้อมูล'}" คิดเป็น ${maxRiskPct}% ของทั้งหมด`;

  const trendInterpretation = `การแปรผล: คะแนนความเครียดเฉลี่ยปัจจุบันอยู่ที่ ${avgSt5.toFixed(1)} คะแนน (จากเต็ม 15) ภาพรวมอยู่ในระดับ${avgSt5 > 7 ? 'ที่ควรเฝ้าระวัง' : 'ปกติ'}`;

  const maxPositive = radarData.reduce((max, current) => current.A > (max?.A || 0) ? current : max, radarData[0]);
  const positiveInterpretation = radarMaxPos === 0 
    ? 'การแปรผล: ปัจจุบันยังไม่พบข้อมูลพฤติกรรมเชิงบวก' 
    : `การแปรผล: จุดแข็งที่พบมากที่สุดคือ "${maxPositive?.subject || 'ไม่มีข้อมูล'}" ควรส่งเสริมเพื่อเป็นปัจจัยปกป้อง`;

  const maxNegative = negativeChartData[0];
  const negativeInterpretation = maxNegative?.count === 0 
    ? 'การแปรผล: ปัจจุบันยังไม่พบพฤติกรรมเสี่ยงที่ต้องเฝ้าระวัง' 
    : `การแปรผล: พฤติกรรมเสี่ยงที่พบสูงสุดคือ "${maxNegative?.name || 'ไม่มีข้อมูล'}" ควรมีมาตรการดูแลอย่างใกล้ชิด`;

  return (
    <div className="space-y-6 md:space-y-8 animate-in fade-in">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 border-b border-slate-200 pb-6">
        <div>
          <h2 className="text-2xl md:text-3xl font-black text-slate-800 flex items-center gap-3">
            <Brain className="text-pink-500" size={36}/> 
            Executive Dashboard
          </h2>
          <p className="text-slate-500 font-medium mt-2">
            ศูนย์บัญชาการข้อมูลสุขภาพจิตและพฤติกรรมเชิงลึกระดับนโยบาย
          </p>
        </div>
      </div>

      {/* FILTER SECTION */}
      <div className="bg-white p-5 md:p-6 rounded-[2.5rem] shadow-sm border border-slate-100 flex flex-col md:flex-row gap-4">
        {profile.role === 'superadmin' && (
          <div className="flex-1">
            <label className="block text-xs font-bold text-slate-500 mb-1.5 pl-1">ตัวกรองหน่วยงาน/สังกัด</label>
            <select 
              className="w-full p-3.5 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-pink-500/20 focus:border-pink-400 outline-none bg-slate-50 hover:bg-white transition-all text-sm font-medium text-slate-700"
              value={selectedAffiliation}
              onChange={handleAffiliationChange}
            >
              <option value="all">✦ ภาพรวมประชากรทั้งหมด</option>
              {availableAffiliations.map((aff, idx) => <option key={idx} value={aff}>{aff}</option>)}
            </select>
          </div>
        )}
        <div className="flex-1">
          <label className="block text-xs font-bold text-slate-500 mb-1.5 pl-1">ตัวกรองเจาะลึกรายบุคคล (Individual View)</label>
          <select 
            className="w-full p-3.5 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-pink-500/20 focus:border-pink-400 outline-none bg-slate-50 hover:bg-white transition-all text-sm font-medium text-slate-700"
            value={selectedUserFilter}
            onChange={e => setSelectedUserFilter(e.target.value)}
          >
            <option value="all">✦ วิเคราะห์แบบประชากรกลุ่ม (Group Profiling)</option>
            {studentsInAffiliation.map(u => <option key={u.id} value={u.id}>{u.name} (@{u.id})</option>)}
          </select>
        </div>
      </div>

      {/* SUB TABS NAVIGATION */}
      <div className="flex bg-slate-100 p-1.5 rounded-3xl w-fit max-w-full overflow-x-auto hide-scrollbar">
        <button onClick={() => setSubTab('overview')} className={`px-5 py-2.5 rounded-2xl text-xs font-bold transition-all whitespace-nowrap flex items-center gap-2 ${subTab === 'overview' ? 'bg-white shadow text-pink-500' : 'text-slate-500'}`}>
          <LayoutDashboard size={16}/> สรุปภาพรวม (KPIs)
        </button>
        <button onClick={() => setSubTab('mental')} className={`px-5 py-2.5 rounded-2xl text-xs font-bold transition-all whitespace-nowrap flex items-center gap-2 ${subTab === 'mental' ? 'bg-white shadow text-pink-500' : 'text-slate-500'}`}>
          <Activity size={16}/> สุขภาพจิต (Mental)
        </button>
        <button onClick={() => setSubTab('behavior')} className={`px-5 py-2.5 rounded-2xl text-xs font-bold transition-all whitespace-nowrap flex items-center gap-2 ${subTab === 'behavior' ? 'bg-white shadow text-pink-500' : 'text-slate-500'}`}>
          <Users size={16}/> พฤติกรรม (Behavior)
        </button>
        <button onClick={() => setSubTab('policy')} className={`px-5 py-2.5 rounded-2xl text-xs font-bold transition-all whitespace-nowrap flex items-center gap-2 ${subTab === 'policy' ? 'bg-white shadow text-pink-500' : 'text-slate-500'}`}>
          <Bot size={16}/> บทวิเคราะห์ AI & นโยบาย
        </button>
      </div>

      {/* TAB 1: EXECUTIVE KPIs (OVERVIEW) */}
      {subTab === 'overview' && (
        <div className="space-y-6 md:space-y-8 animate-in fade-in">
          {/* Top KPI Grid */}
          <div className="grid grid-cols-2 lg:grid-cols-6 gap-4">
            <div className="col-span-2 bg-gradient-to-br from-indigo-500 to-purple-600 p-6 rounded-[2rem] shadow-lg shadow-indigo-200 text-white flex flex-col justify-center">
              <p className="text-indigo-100 font-medium text-sm">Well-being Score (ดัชนีความสุขรวม)</p>
              <div className="flex items-end gap-2 mt-2">
                <p className="text-6xl font-black">{wellbeingScore.toFixed(0)}</p>
                <p className="text-xl font-bold mb-1 opacity-80">/ 100</p>
              </div>
              <p className="text-xs mt-3 text-indigo-100 bg-white/10 p-2 rounded-xl border border-white/20">คำนวณจากความเครียดเชิงลบและพฤติกรรมเชิงบวกสุทธิ</p>
            </div>

            <div className="bg-white p-5 rounded-[2rem] shadow-sm border border-slate-100 flex flex-col items-center justify-center text-center">
              <Users size={24} className="text-slate-400 mb-2"/>
              <p className="text-2xl font-black text-slate-700">{totalEvaluated}</p>
              <p className="text-[10px] font-bold text-slate-400 uppercase mt-1">ผู้ตอบแบบประเมิน</p>
            </div>
            
            <div className="bg-white p-5 rounded-[2rem] shadow-sm border border-slate-100 flex flex-col items-center justify-center text-center border-b-4 border-b-rose-400">
              <Flame size={24} className="text-rose-400 mb-2"/>
              <p className="text-2xl font-black text-rose-500">{pctHighStress}%</p>
              <p className="text-[10px] font-bold text-slate-400 uppercase mt-1">เครียดสูง-วิกฤต</p>
            </div>

            <div className="bg-white p-5 rounded-[2rem] shadow-sm border border-slate-100 flex flex-col items-center justify-center text-center border-b-4 border-b-orange-400">
              <ShieldOff size={24} className="text-orange-400 mb-2"/>
              <p className="text-2xl font-black text-orange-500">{pctBullying}%</p>
              <p className="text-[10px] font-bold text-slate-400 uppercase mt-1">Bullying</p>
            </div>

            <div className="bg-white p-5 rounded-[2rem] shadow-sm border border-slate-100 flex flex-col items-center justify-center text-center border-b-4 border-b-sky-400">
              <Gamepad2 size={24} className="text-sky-400 mb-2"/>
              <p className="text-2xl font-black text-sky-500">{pctGaming}%</p>
              <p className="text-[10px] font-bold text-slate-400 uppercase mt-1">ติดเกม/สื่อ</p>
            </div>
            
            <div className="bg-white p-5 rounded-[2rem] shadow-sm border border-slate-100 flex flex-col items-center justify-center text-center border-b-4 border-b-amber-500">
              <Footprints size={24} className="text-amber-500 mb-2"/>
              <p className="text-2xl font-black text-amber-600">{pctTruancy}%</p>
              <p className="text-[10px] font-bold text-slate-400 uppercase mt-1">หนีเรียน</p>
            </div>
            
            <div className="bg-white p-5 rounded-[2rem] shadow-sm border border-slate-100 flex flex-col items-center justify-center text-center border-b-4 border-b-red-600">
              <AlertCircle size={24} className="text-red-500 mb-2"/>
              <p className="text-2xl font-black text-red-600">{pctSubstance}%</p>
              <p className="text-[10px] font-bold text-slate-400 uppercase mt-1">สารเสพติด</p>
            </div>
          </div>

          {/* AI Insights Highlights */}
          <div className="bg-gradient-to-r from-pink-50 to-purple-50 p-6 md:p-8 rounded-[2.5rem] border border-pink-100">
            <h3 className="font-black text-lg text-pink-700 flex items-center gap-2 mb-4">
              <Bot className="text-pink-500" size={24}/> AI Auto-Generated Insights (ข้อค้นพบอัตโนมัติ)
            </h3>
            <div className="space-y-3">
              {aiInsightTexts.map((text, i) => (
                <div key={i} className="flex gap-3 bg-white/60 p-4 rounded-2xl shadow-sm border border-white">
                  <Sparkles className="text-purple-400 shrink-0 mt-0.5" size={18} />
                  <p className="text-sm font-medium text-slate-700 leading-relaxed">{text}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: MENTAL HEALTH */}
      {subTab === 'mental' && (
        <div className="space-y-6 md:space-y-8 animate-in fade-in">
           <div className="grid lg:grid-cols-2 gap-6">
              {/* ST-5 Bar Chart */}
              <div className="bg-white p-6 md:p-8 rounded-[2.5rem] shadow-sm border border-slate-100">
                <h3 className="font-black text-base text-slate-800 flex items-center gap-2 mb-6"><BarChart3 className="text-teal-400"/> ST-5 Distribution (การกระจายตัวของความเครียด)</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartDataRisk} layout="vertical" margin={{ top: 0, right: 20, left: 0, bottom: 0 }}>
                      <XAxis type="number" hide />
                      <YAxis dataKey="name" type="category" axisLine={false} tickLine={false} fontSize={12} fontWeight="bold" fill="#64748b" width={110}/>
                      <Tooltip cursor={{fill: '#f8fafc'}} contentStyle={{borderRadius: '16px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)'}}/>
                      <Bar dataKey="count" radius={[0, 16, 16, 0]} barSize={28}>
                        {chartDataRisk.map((entry, index) => <Cell key={`cell-${index}`} fill={entry.fill} />)}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
                <div className="mt-4 p-4 bg-teal-50/50 rounded-2xl border border-teal-100">
                  <p className="text-sm font-medium text-teal-800">{st5Interpretation}</p>
                </div>
              </div>
              
              {/* Trend / Timeline Mockup (Using line chart of recent assessments) */}
              <div className="bg-white p-6 md:p-8 rounded-[2.5rem] shadow-sm border border-slate-100">
                <h3 className="font-black text-base text-slate-800 flex items-center gap-2 mb-6"><TrendingUp className="text-indigo-400"/> Stress Trend (แนวโน้มคะแนนเฉลี่ยล่าสุด)</h3>
                <div className="h-64 flex flex-col justify-center items-center bg-slate-50 rounded-2xl border border-slate-100">
                   {/* Normally we'd map timestamps to dates. For simplicity, just showing an area chart illustration */}
                   <ResponsiveContainer width="90%" height="80%">
                      <AreaChart data={[
                        { name: 'W1', score: 4 }, { name: 'W2', score: 6 }, { name: 'W3', score: 5 }, { name: 'W4', score: 8 }, { name: 'W5', score: avgSt5 }
                      ]}>
                        <defs>
                          <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                            <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                          </linearGradient>
                        </defs>
                        <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fontSize: 10, fill:'#94a3b8'}} />
                        <YAxis hide domain={[0, 15]}/>
                        <Tooltip contentStyle={{borderRadius: '12px', border: 'none'}}/>
                        <Area type="monotone" dataKey="score" stroke="#8b5cf6" strokeWidth={3} fillOpacity={1} fill="url(#colorScore)" />
                      </AreaChart>
                   </ResponsiveContainer>
                   <p className="text-[10px] text-slate-400 mt-2 font-bold">กราฟจำลองการเคลื่อนไหวของความเครียดในช่วง 5 ครั้งล่าสุด</p>
                </div>
                <div className="mt-4 p-4 bg-indigo-50/50 rounded-2xl border border-indigo-100">
                  <p className="text-sm font-medium text-indigo-800">{trendInterpretation}</p>
                </div>
              </div>
           </div>

           {/* High Risk Group List */}
           <div className="bg-rose-50 p-6 md:p-8 rounded-[2.5rem] border border-rose-100">
              <h3 className="font-black text-lg text-rose-700 flex items-center gap-2 mb-4"><ShieldAlert size={20}/> กลุ่มเสี่ยงสูง (High Risk Group - เฝ้าระวังพิเศษ)</h3>
              
              {(() => {
                const highRiskStudents = validForCorrelation.filter(d => ['High', 'Severe'].includes(d.riskGroup));
                if (highRiskStudents.length === 0) {
                  return <p className="text-rose-400 text-sm font-medium">ไม่พบผู้ประเมินที่อยู่ในเกณฑ์ความเสี่ยงสูง</p>;
                }
                
                // จัดกลุ่มตามสังกัด/สถานที่
                const grouped: Record<string, any[]> = highRiskStudents.reduce((acc: any, u) => {
                  const aff = u.affiliation || 'ไม่ระบุสังกัด/สถานที่';
                  if (!acc[aff]) acc[aff] = [];
                  acc[aff].push(u);
                  return acc;
                }, {});

                return (
                  <div className="space-y-6 max-h-96 overflow-y-auto custom-scrollbar pr-2">
                    {Object.entries(grouped).map(([affiliation, studentsList]) => (
                      <div key={affiliation} className="space-y-3">
                        {/* หัวข้อสังกัด */}
                        <div className="flex items-center gap-2 pb-1 border-b border-rose-100">
                          <span className="w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse"></span>
                          <h4 className="font-bold text-sm text-rose-800 tracking-tight flex items-center gap-2">
                            {affiliation}
                            <span className="text-xs bg-rose-200/50 text-rose-700 px-2 py-0.5 rounded-full font-black">
                              {studentsList.length} คน
                            </span>
                          </h4>
                        </div>
                        
                        {/* รายการผู้เรียนกลุ่มเสี่ยงสูง */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          {studentsList.map((u, idx) => (
                            <div 
                              key={idx} 
                              onClick={() => setSelectedStudentForDetail(u)}
                              className="bg-white p-4 rounded-2xl shadow-sm border border-rose-100 flex justify-between items-center hover:border-rose-300 hover:shadow-md cursor-pointer transition-all transform hover:-translate-y-0.5"
                              title="คลิกเพื่อดูรายละเอียดการประเมิน"
                            >
                              <div>
                                <p className="font-bold text-slate-700 text-sm">{u.name}</p>
                                <div className="flex items-center gap-2 mt-1.5 flex-wrap">
                                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md ${
                                    u.riskGroup === 'Severe' 
                                      ? 'bg-rose-100 text-rose-700 border border-rose-200' 
                                      : 'bg-amber-100 text-amber-700 border border-amber-200'
                                  }`}>
                                    ST-5: {u.st5Score} ({u.riskGroup === 'Severe' ? 'เครียดรุนแรง' : 'เครียดสูง'})
                                  </span>
                                  {u.totalBadBehaviors > 0 && (
                                    <span className="text-[10px] font-bold bg-orange-50 text-orange-600 px-2 py-0.5 rounded-md border border-orange-100">
                                      พฤติกรรมเสี่ยง: {u.totalBadBehaviors}
                                    </span>
                                  )}
                                </div>
                              </div>
                              <span className={`w-8 h-8 rounded-full flex items-center justify-center font-black text-xs ${
                                u.riskGroup === 'Severe'
                                  ? 'bg-rose-100 text-rose-600'
                                  : 'bg-amber-100 text-amber-600'
                              }`}>
                                !
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                );
              })()}
           </div>
        </div>
      )}

      {/* TAB 3: BEHAVIOR */}
      {subTab === 'behavior' && (
        <div className="space-y-6 md:space-y-8 animate-in fade-in">
          <div className="grid lg:grid-cols-2 gap-6">
            
            {/* Radar Chart (Positive Behaviors) */}
            <div className="bg-white p-6 md:p-8 rounded-[2.5rem] shadow-sm border border-slate-100 flex flex-col items-center">
              <div className="w-full flex justify-between items-center mb-2">
                <h3 className="font-black text-base text-slate-800 flex items-center gap-2"><CheckCircle2 className="text-teal-400"/> Positive Behavior Radar</h3>
              </div>
              <p className="text-xs text-slate-400 w-full mb-4">จุดแข็งและศักยภาพของเป้าหมาย (Protective Factors)</p>
              
              <div className="w-full h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                    <PolarGrid stroke="#e2e8f0" />
                    <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 10, fontWeight: 'bold' }} />
                    <PolarRadiusAxis angle={30} domain={[0, radarDomainMax]} tick={false} axisLine={false}/>
                    <Radar name="ความถี่พฤติกรรมเชิงบวก" dataKey="A" stroke="#14b8a6" fill="#14b8a6" fillOpacity={radarMaxPos === 0 ? 0 : 0.4} strokeOpacity={radarMaxPos === 0 ? 0 : 1} />
                    <Tooltip contentStyle={{borderRadius: '12px', border: 'none'}}/>
                  </RadarChart>
                </ResponsiveContainer>
              </div>
              <div className="w-full mt-4 p-4 bg-teal-50/50 rounded-2xl border border-teal-100">
                <p className="text-sm font-medium text-teal-800">{positiveInterpretation}</p>
              </div>
            </div>

            {/* Negative Behavior Heatmap/Bar */}
            <div className="bg-white p-6 md:p-8 rounded-[2.5rem] shadow-sm border border-slate-100">
               <h3 className="font-black text-base text-slate-800 flex items-center gap-2 mb-2"><AlertCircle className="text-rose-400"/> Negative Behavior Distribution</h3>
               <p className="text-xs text-slate-400 w-full mb-6">จัดอันดับความถี่ของพฤติกรรมเสี่ยงและปัญหา (Risk Factors)</p>
               
               <div className="space-y-4">
                  {negativeChartData.map((item, idx) => {
                    const maxCount = negativeChartData[0]?.count || 1;
                    const pct = (item.count / maxCount) * 100;
                    // Color Heatmap logic: Red for top, orange/amber for lower
                    let barColor = "bg-rose-500";
                    if (idx > 0 && pct < 70) barColor = "bg-orange-400";
                    if (idx > 2 && pct < 40) barColor = "bg-amber-300";
                    if (item.count === 0) barColor = "bg-slate-200";

                    return (
                      <div key={idx} className="relative">
                        <div className="flex justify-between text-xs font-bold text-slate-700 mb-1.5">
                          <span>{item.name}</span>
                          <span>{item.count} ครั้ง</span>
                        </div>
                        <div className="w-full h-3 bg-slate-100 rounded-full overflow-hidden">
                          <div className={`h-full ${barColor} rounded-full transition-all duration-1000`} style={{width: `${item.count === 0 ? 0 : pct}%`}}></div>
                        </div>
                      </div>
                    )
                  })}
               </div>
               <div className="mt-6 p-4 bg-rose-50/50 rounded-2xl border border-rose-100">
                  <p className="text-sm font-medium text-rose-800">{negativeInterpretation}</p>
               </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 4: POLICY & ACTION PLAN */}
      {subTab === 'policy' && (
        <div className="space-y-6 md:space-y-8 animate-in fade-in">
          {/* Executive Summary Report Card */}
          <div className="bg-white p-6 md:p-8 rounded-[2.5rem] shadow-sm border border-slate-100 space-y-4">
            <h3 className="font-black text-lg text-slate-800 flex items-center gap-2"><FileText className="text-indigo-400"/> {isIndividualMode ? 'รายงานการวิเคราะห์สรุปเคส (Case Formulation)' : 'รายงานสรุปผลสัมฤทธิ์ทางการประเมินผู้บริหาร'}</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="space-y-3.5 text-xs text-slate-600 leading-relaxed">
                <p className="font-bold text-sm text-slate-700">✦ สรุปประเด็นข้อค้นพบสำคัญ (Key Findings):</p>
                {isIndividualMode ? (
                  <ul className="space-y-2.5 list-decimal pl-4">
                    <li><strong>ภาพรวมความเครียด (ST-5):</strong> ผลประเมินล่าสุดของนักเรียนอยู่เกณฑ์ <strong>"{aggregatedData[0]?.riskGroup}"</strong> (ระดับคะแนน {aggregatedData[0]?.st5Score}) ซึ่งสะท้อนถึงสภาวะอารมณ์ในปัจจุบัน</li>
                    <li><strong>พฤติกรรมเฝ้าระวังสะสม:</strong> พบรายการพฤติกรรมที่ต้องเฝ้าระวังรวม <strong>{aggregatedData[0]?.totalBadBehaviors} รายการ</strong> จากการประเมินในระบบ</li>
                  </ul>
                ) : (
                  <ul className="space-y-2.5 list-decimal pl-4">
                    <li><strong>Well-being Score:</strong> ดัชนีความสุขมวลรวมประชากรอยู่ที่ <strong>{wellbeingScore.toFixed(0)}/100</strong> คะแนน</li>
                    <li><strong>Coverage Analysis:</strong> อัตราการคัดกรองด้วยแบบประเมิน ST-5 อยู่ที่ <strong>{coverageSt5.toFixed(1)}%</strong></li>
                    <li><strong>High Risk Ratio:</strong> มีกลุ่มที่เผชิญความเครียดสูงถึงวิกฤต จำนวน {countHighStress} ราย (คิดเป็น {pctHighStress}%) ซึ่งต้องได้รับการดูแลอย่างเร่งด่วน</li>
                  </ul>
                )}
              </div>
              
              <div className="space-y-3.5 text-xs text-slate-600 leading-relaxed">
                <p className="font-bold text-sm text-slate-700">✦ {isIndividualMode ? 'ข้อเสนอแนะการช่วยเหลือ (Intervention Guidelines):' : 'ข้อเสนอแนะเชิงนโยบาย (Policy Recommendations):'}</p>
                {isIndividualMode ? (
                  <ul className="space-y-2.5 list-disc pl-4">
                    <li><strong>รับฟังอย่างตั้งใจ:</strong> เปิดโอกาสให้นักเรียนระบายความรู้สึกในพื้นที่ที่ปลอดภัย ปราศจากการตัดสินหรือการตำหนิ (Non-judgmental approach)</li>
                    <li><strong>ปรับพฤติกรรมผ่านกิจกรรม:</strong> ดึงจุดเด่นพฤติกรรมเชิงบวกของเด็กมาเป็นตัวตั้ง เพื่อสร้าง Self-esteem ทดแทนปัญหาเดิม</li>
                  </ul>
                ) : (
                  <ul className="space-y-2.5 list-disc pl-4">
                    <li><strong>นโยบายเยียวยาเชิงบวกเป็นมิตร:</strong> มุ่งเน้นการสร้างเสริมพฤติกรรมพึงประสงค์ (Positive Behavioral Intervention) มากกว่าการลงโทษ</li>
                    <li><strong>Early Warning System:</strong> ให้ความสำคัญกับการสังเกตพฤติกรรม "หนีเรียน" และ "ติดสื่อ" เป็นตัวบ่งชี้ความเครียดแฝงเพื่อเข้าแทรกแซงล่วงหน้า</li>
                  </ul>
                )}
              </div>
            </div>
          </div>

          {/* Action Plans */}
          <div className="bg-white p-6 md:p-8 rounded-[2.5rem] shadow-sm border border-slate-100 space-y-6">
            <h3 className="font-black text-lg text-slate-800 flex items-center gap-2"><BookOpen className="text-purple-400"/> {isIndividualMode ? 'แผนปฏิบัติการดูแลรายบุคคล (Individualized Action Plan)' : 'แผนปฏิบัติการตามกรอบเวลา (Mini Flag Ship Satun Action Plan)'}</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-teal-50/50 p-6 rounded-3xl border border-teal-100/50 space-y-3">
                <div className="w-10 h-10 bg-teal-100 text-teal-600 rounded-xl flex items-center justify-center">
                  <Star size={20}/>
                </div>
                <h4 className="font-bold text-teal-800 text-sm">ระยะสั้น (1 เดือน)</h4>
                <p className="text-xs text-slate-600 leading-relaxed">
                  {isIndividualMode
                    ? "ครูประจำชั้นจัดเวลาพูดคุยสอบถามสารทุกข์สุกดิบอย่างน้อย 1 ครั้ง/สัปดาห์ พร้อมทำความเข้าใจเงื่อนไขแวดล้อมที่ส่งผลต่ออารมณ์ในปัจจุบัน"
                    : "เร่งคัดกรองให้ครบถ้วน 100% ทั่วถึงกลุ่มที่ข้อมูลสูญหาย จัดตั้งระบบ Triage คัดแยก และส่งทีมครูเข้าดูแลใกล้ชิดรายบุคคลกับกลุ่มเสี่ยงรุนแรงทันที"}
                </p>
              </div>

              <div className="bg-indigo-50/50 p-6 rounded-3xl border border-indigo-100/50 space-y-3">
                <div className="w-10 h-10 bg-indigo-100 text-indigo-600 rounded-xl flex items-center justify-center">
                  <Sparkles size={20}/>
                </div>
                <h4 className="font-bold text-indigo-800 text-sm">ระยะกลาง (3-6 เดือน)</h4>
                <p className="text-xs text-slate-600 leading-relaxed">
                  {isIndividualMode
                    ? "ประเมิน ST-5 ซ้ำเพื่อดูแนวโน้ม หากระดับความเครียดยังคงอยู่ในเกณฑ์วิกฤต (>=8) ให้พิจารณาส่งต่อข้อมูลให้ทีมงานสาธารณสุขระดับชุมชน"
                    : "จัดอบรมเชิงปฏิบัติการพัฒนาทักษะชีวิต (Life Skills) ควบคุมสมาธิ และการผ่อนคลายความตึงเครียดร่วมกับกิจกรรมชุมชน เน้นกลุ่มเปราะบาง"}
                </p>
              </div>

              <div className="bg-purple-50/50 p-6 rounded-3xl border border-purple-100/50 space-y-3">
                <div className="w-10 h-10 bg-purple-100 text-purple-600 rounded-xl flex items-center justify-center">
                  <HelpCircle size={20}/>
                </div>
                <h4 className="font-bold text-purple-800 text-sm">ระยะยาว (1 ปี)</h4>
                <p className="text-xs text-slate-600 leading-relaxed">
                  {isIndividualMode
                    ? "สร้างความภาคภูมิใจในตนเอง (Self-esteem) สนับสนุนให้ค้นพบศักยภาพ และดึงศักยภาพนั้นมาใช้ให้เกิดประโยชน์ในระดับโรงเรียน"
                    : "พัฒนานวัตกรรมส่งต่อข้อมูลเชิงระบาดวิทยาถาวร เพื่อประเมินดัชนีชี้วัดความสุขมวลรวม (Well-being Score) ของประชากรในโครงการระยะยาว"}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* POPUP MODAL: รายละเอียดกลุ่มเฝ้าระวังพิเศษ (High Risk Student Detail) */}
      {selectedStudentForDetail && (
        <div className="fixed inset-0 z-40 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-in fade-in duration-200 overflow-y-auto text-left">
          <div className="relative w-full max-w-4xl bg-white border-2 border-rose-100 p-6 md:p-8 rounded-[2.5rem] shadow-2xl space-y-6 my-8 max-h-[90vh] overflow-y-auto custom-scrollbar animate-in zoom-in-95 duration-300">
            {/* Close button */}
            <button 
              onClick={() => setSelectedStudentForDetail(null)} 
              className="absolute top-4 right-4 p-2 text-slate-400 hover:text-rose-500 hover:bg-rose-50 rounded-full transition-all"
            >
              <XCircle size={28} />
            </button>

            {/* Header */}
            <div className="flex items-center gap-4 border-b pb-4">
              <div className="w-14 h-14 bg-gradient-to-br from-rose-100 to-rose-200 text-rose-600 rounded-full flex items-center justify-center text-xl font-black shadow-inner border border-rose-200">
                {selectedStudentForDetail.name.charAt(0)}
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h4 className="font-black text-xl text-slate-800">{selectedStudentForDetail.name}</h4>
                  <span className="text-[10px] font-bold bg-rose-100 text-rose-700 px-2.5 py-0.5 rounded-full border border-rose-200">กลุ่มเฝ้าระวังพิเศษ</span>
                </div>
                <p className="text-xs text-slate-500 mt-1.5">
                  ID: {selectedStudentForDetail.uid} • สังกัด: {selectedStudentForDetail.affiliation}
                </p>
              </div>
            </div>

            {/* รายละเอียดคำตอบรายข้อล่าสุดตามเกณฑ์ประเมินสำหรับแอดมิน */}
            {(() => {
              const uSt5 = [...st5Data.filter((d: any) => d.uid === selectedStudentForDetail.uid || d.userId === selectedStudentForDetail.uid)].sort((a: any, b: any) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
              if (uSt5.length === 0) return null;
              const latest = uSt5[0];
              const status = calculateST5(latest.score);

              return (
                <div className="bg-slate-50 p-5 rounded-3xl border border-slate-100 space-y-4">
                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
                    <div className="flex items-center gap-2">
                      <span className="w-3 h-3 rounded-full bg-purple-500 animate-pulse animate-duration-1000"></span>
                      <h5 className="font-black text-sm text-slate-800">
                        วิเคราะห์คำตอบรายข้อล่าสุด (ประเมินเมื่อ {new Date(latest.timestamp).toLocaleDateString('th-TH')})
                      </h5>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`px-3 py-1 rounded-full text-xs font-black border shadow-sm ${status.color}`}>
                        คะแนนรวม: {latest.score} แต้ม ({status.level})
                      </span>
                    </div>
                  </div>

                  {latest.answers && latest.answers.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {/* กลุ่มที่ไม่ผ่านเกณฑ์ (ความเสี่ยงสูง) */}
                      <div className="bg-rose-50/50 p-4 rounded-2xl border border-rose-100/50 space-y-3">
                        <div className="flex items-center gap-2 text-rose-700 font-bold text-xs pb-1 border-b border-rose-100">
                          <AlertCircle size={15} />
                          <span>ไม่ผ่านเกณฑ์ (มีอาการบ่อยครั้ง - เป็นประจำ)</span>
                          <span className="ml-auto bg-rose-100 text-rose-800 px-2 py-0.5 rounded-full text-[10px] font-black">
                            {st5Questions.filter((_, idx) => (latest.answers[idx] !== undefined ? latest.answers[idx] : 0) >= 2).length} ข้อ
                          </span>
                        </div>
                        <div className="space-y-2">
                          {st5Questions.map((q, idx) => {
                            const val = latest.answers[idx] !== undefined ? latest.answers[idx] : 0;
                            if (val < 2) return null;
                            const optLabel = st5Options.find(o => o.value === val)?.label || `คะแนน ${val}`;
                            return (
                              <div key={idx} className="bg-white p-3 rounded-xl border border-rose-100 flex items-start gap-2 text-xs">
                                <span className="w-5 h-5 rounded-full bg-rose-100 text-rose-700 flex items-center justify-center font-black shrink-0 text-[10px]">{idx + 1}</span>
                                <div className="space-y-0.5">
                                  <p className="font-bold text-slate-700 leading-snug">{q}</p>
                                  <p className="text-rose-600 font-semibold text-[10px]">ระดับอาการ: {optLabel}</p>
                                </div>
                              </div>
                            );
                          })}
                          {st5Questions.filter((_, idx) => (latest.answers[idx] !== undefined ? latest.answers[idx] : 0) >= 2).length === 0 && (
                            <p className="text-xs text-rose-400 italic text-center py-2">ไม่มีข้อที่ไม่ผ่านเกณฑ์ประเมิน</p>
                          )}
                        </div>
                      </div>

                      {/* กลุ่มที่ผ่านเกณฑ์ (ปกติ) */}
                      <div className="bg-teal-50/50 p-4 rounded-2xl border border-teal-100/50 space-y-3">
                        <div className="flex items-center gap-2 text-teal-700 font-bold text-xs pb-1 border-b border-teal-100">
                          <CheckCircle2 size={15} />
                          <span>ผ่านเกณฑ์ (ปกติ - มีอาการบางครั้ง)</span>
                          <span className="ml-auto bg-teal-100 text-teal-800 px-2 py-0.5 rounded-full text-[10px] font-black">
                            {st5Questions.filter((_, idx) => (latest.answers[idx] !== undefined ? latest.answers[idx] : 0) < 2).length} ข้อ
                          </span>
                        </div>
                        <div className="space-y-2">
                          {st5Questions.map((q, idx) => {
                            const val = latest.answers[idx] !== undefined ? latest.answers[idx] : 0;
                            if (val >= 2) return null;
                            const optLabel = st5Options.find(o => o.value === val)?.label || `คะแนน ${val}`;
                            return (
                              <div key={idx} className="bg-white p-3 rounded-xl border border-teal-100 flex items-start gap-2 text-xs opacity-90">
                                <span className="w-5 h-5 rounded-full bg-teal-100 text-teal-700 flex items-center justify-center font-black shrink-0 text-[10px]">{idx + 1}</span>
                                <div className="space-y-0.5">
                                  <p className="font-bold text-slate-700 leading-snug">{q}</p>
                                  <p className="text-teal-600 font-semibold text-[10px]">ระดับอาการ: {optLabel}</p>
                                </div>
                              </div>
                            );
                          })}
                          {st5Questions.filter((_, idx) => (latest.answers[idx] !== undefined ? latest.answers[idx] : 0) < 2).length === 0 && (
                            <p className="text-xs text-teal-400 italic text-center py-2">ไม่มีข้อที่ผ่านเกณฑ์ประเมิน</p>
                          )}
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="p-4 bg-white rounded-2xl border border-slate-100 text-center">
                      <p className="text-xs text-slate-500 font-medium">
                        ข้อมูลนี้ถูกนำเข้าด้วยคะแนนรวมความเครียด <span className="font-black text-rose-600">{latest.score} แต้ม</span> (ไม่ได้ระบุรายละเอียดรายข้อในฐานข้อมูลหลัก)
                      </p>
                      <p className="text-[11px] text-slate-400 mt-1">
                        ข้อแนะนำเบื้องต้น: สภาวะโดยทั่วไปเข้าเกณฑ์ความเสี่ยงวิกฤต ควรประสานส่งต่อตามนโยบายสุขภาพจิต
                      </p>
                    </div>
                  )}
                </div>
              );
            })()}

            {/* Content body */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Column 1: ST-5 History */}
              <div className="space-y-4">
                <h5 className="font-black text-sm text-slate-700 flex items-center gap-2 border-b pb-2">
                  <HeartPulse size={18} className="text-pink-500" /> ประวัติประเมินสุขภาพจิต (ST-5)
                </h5>
                <div className="space-y-3 max-h-[350px] overflow-y-auto pr-1">
                  {(() => {
                    const uSt5 = [...st5Data.filter((d: any) => d.uid === selectedStudentForDetail.uid || d.userId === selectedStudentForDetail.uid)].sort((a: any, b: any) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
                    if (uSt5.length === 0) return <p className="text-slate-400 text-xs py-4 text-center">ไม่พบข้อมูลประเมินสุขภาพจิต</p>;
                    return uSt5.map((item: any, idx: number) => {
                      const status = calculateST5(item.score);
                      return (
                        <div key={item.id} className="p-4 border border-slate-100 rounded-2xl bg-slate-50/50 flex justify-between items-center gap-3">
                          <div>
                            <p className="text-xs font-bold text-slate-600">ครั้งที่ {uSt5.length - idx}</p>
                            <p className="text-[10px] text-slate-400 mt-0.5">{new Date(item.timestamp).toLocaleDateString('th-TH')}</p>
                          </div>
                          <div className="flex items-center gap-2">
                            <button 
                              onClick={() => setViewingSt5Result({ score: item.score, answers: item.answers, ...status })}
                              className="text-[10px] bg-white text-purple-600 px-2.5 py-1 border border-purple-200 rounded-full hover:bg-purple-50 transition font-bold shadow-sm"
                            >
                              ดูแนวทาง
                            </button>
                            <span className={`px-3 py-1 rounded-full text-[10px] font-bold border shadow-sm ${status.color}`}>
                              {status.level} ({item.score} แต้ม)
                            </span>
                          </div>
                        </div>
                      );
                    });
                  })()}
                </div>
              </div>

              {/* Column 2: Behavior History */}
              <div className="space-y-4">
                <h5 className="font-black text-sm text-slate-700 flex items-center gap-2 border-b pb-2">
                  <ClipboardList size={18} className="text-teal-500" /> ประวัติพฤติกรรม (Behavioral Log)
                </h5>
                <div className="space-y-3 max-h-[350px] overflow-y-auto pr-1">
                  {(() => {
                    const uBeh = [...behaviorData.filter((d: any) => d.targetUid === selectedStudentForDetail.uid)].sort((a: any, b: any) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
                    if (uBeh.length === 0) return <p className="text-slate-400 text-xs py-4 text-center">ไม่พบข้อมูลประวัติพฤติกรรม</p>;
                    return uBeh.map((item: any, idx: number) => (
                      <div key={item.id || idx} className="p-4 border border-slate-100 rounded-2xl bg-slate-50/50 flex justify-between items-center gap-3">
                        <div>
                          <p className="text-xs font-bold text-slate-600">ประเมินเมื่อ {new Date(item.timestamp).toLocaleDateString('th-TH')}</p>
                          <p className="text-[10px] text-slate-400 mt-0.5">โดยครู/ผู้รับผิดชอบ</p>
                        </div>
                        <div className="flex items-center gap-2">
                          <button 
                            onClick={() => setViewingBehaviorResult(item.selections)}
                            className="text-[10px] bg-white text-teal-600 px-2.5 py-1 border border-teal-200 rounded-full hover:bg-teal-50 transition font-bold shadow-sm"
                          >
                            ดูข้อเสนอแนะ
                          </button>
                          <div className="flex gap-1">
                            {item.selections?.undesirable?.length > 0 && (
                              <span className="bg-rose-50 border border-rose-100 text-rose-700 font-bold text-[9px] px-1.5 py-0.5 rounded">
                                เสี่ยง {item.selections.undesirable.length}
                              </span>
                            )}
                            {item.selections?.desirable?.length > 0 && (
                              <span className="bg-teal-50 border border-teal-100 text-teal-700 font-bold text-[9px] px-1.5 py-0.5 rounded">
                                บวก {item.selections.desirable.length}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    ));
                  })()}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ST-5 nested modal overlay */}
      {viewingSt5Result && (
        <ST5ResultModal result={viewingSt5Result} isTeacherView={true} onSummaryClose={() => setViewingSt5Result(null)} />
      )}

      {/* Behavior nested modal overlay */}
      {viewingBehaviorResult && (
        <BehaviorResultSummary selections={viewingBehaviorResult} onSummaryClose={() => setViewingBehaviorResult(null)} />
      )}
    </div>
  );
}

// ==========================================
// FORM COMPONENTS
// ==========================================
function ST5Form({ onSubmit, onCancel, initialData }) {
  const [answers, setAnswers] = useState(initialData?.answers || Array(5).fill(null));
  const isComplete = answers.every(a => a !== null);
  const totalScore = answers.reduce((a, b) => a + (b || 0), 0);

  return (
    <div className="bg-white p-6 md:p-10 rounded-[2.5rem] shadow-xl shadow-slate-200/40 border border-slate-100 max-w-3xl mx-auto animate-in fade-in zoom-in-95 duration-300">
      <div className="text-center mb-8">
         <h3 className="text-2xl font-black mb-2 text-slate-800">แบบประเมินความเครียด (ST-5)</h3>
         <span className="bg-pink-100 text-pink-600 px-4 py-2 rounded-full text-sm font-medium border border-pink-200">ในช่วง 2-4 สัปดาห์ที่ผ่านมา ท่านมีอาการเหล่านี้บ่อยแค่ไหน?</span>
      </div>
      
      <div className="space-y-4">
        {st5Questions.map((q, idx) => (
          <div key={idx} className="bg-slate-50 p-5 md:p-6 rounded-3xl border border-slate-100 transition hover:border-sky-200">
            <p className="font-bold text-slate-700 mb-4 text-base">{idx + 1}. {q}</p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2 md:gap-3">
              {st5Options.map(opt => (
                <button key={opt.value} onClick={() => { const n = [...answers]; n[idx] = opt.value; setAnswers(n); }}
                  className={`p-3 text-sm rounded-2xl font-bold transition-all duration-200 ${
                    answers[idx] === opt.value 
                      ? 'bg-sky-400 text-white shadow-md transform scale-105' 
                      : 'bg-white text-slate-500 border border-slate-200 hover:border-sky-300 hover:bg-sky-50'
                  }`}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-10 flex flex-col-reverse md:flex-row gap-4 pt-8 border-t border-slate-100">
        <button onClick={onCancel} className="flex-1 py-4 bg-slate-100 rounded-2xl text-slate-500 hover:bg-slate-200 font-bold transition">ยกเลิก</button>
        <button onClick={() => onSubmit(answers, totalScore)} disabled={!isComplete}
          className="flex-[2] py-4 bg-gradient-to-r from-sky-400 to-indigo-400 text-white rounded-2xl font-bold hover:opacity-90 disabled:opacity-40 disabled:from-slate-300 disabled:to-slate-300 shadow-lg shadow-sky-200 transition text-lg"
        >
          บันทึกผลการประเมิน 🌟
        </button>
      </div>
    </div>
  );
}

function BehaviorForm({ targetUser, onDone, initialData, st5History = [], behaviorHistory = [], triggerAlert }) {
  const [selections, setSelections] = useState(() => {
    if (initialData && initialData.selections) {
      return {
        desirable: initialData.selections.desirable || [],
        undesirable: initialData.selections.undesirable || []
      };
    }
    return { desirable: [], undesirable: [] };
  });
  const [st5RoundId, setSt5RoundId] = useState(
    initialData?.st5RoundId || ''
  );

  const toggleSelection = (type, item) => {
    setSelections(prev => {
      const current = prev[type];
      return current.includes(item) 
        ? { ...prev, [type]: current.filter(i => i !== item) }
        : { ...prev, [type]: [...current, item] };
    });
  };

  const handleSave = async () => {
    const timestamp = initialData ? initialData.timestamp : Date.now();
    const payload = { 
      targetUid: targetUser.id, 
      targetName: targetUser.name, 
      selections: selections || { desirable: [], undesirable: [] },
      desirable: (selections?.desirable || []).join(', '),
      undesirable: (selections?.undesirable || []).join(', '),
      timestamp, 
      st5RoundId 
    };
    
    if (initialData && initialData.id) {
      // โหมดแก้ไข
      await updateDoc(doc(db, 'artifacts', appId, 'public', 'data', 'behaviors', initialData.id), { selections, st5RoundId });
      syncToGoogleSheet('EDIT_BEHAVIOR', payload);
    } else {
      // โหมดสร้างใหม่
      await addDoc(collection(db, 'artifacts', appId, 'public', 'data', 'behaviors'), payload);
      syncToGoogleSheet('BEHAVIOR', payload);
    }
    
    onDone();
  };

  const renderSection = (type, categories, colorTheme) => (
    <div className={`p-6 rounded-[2rem] border-2 mb-6 ${colorTheme.bg} ${colorTheme.border}`}>
      <h3 className={`text-lg font-black mb-6 flex items-center gap-2 ${colorTheme.text}`}>
        {type === 'desirable' ? <CheckCircle2 className="fill-teal-100"/> : <AlertCircle className="fill-rose-100"/>} 
        {type === 'desirable' ? 'พฤติกรรมที่น่าชื่นชม' : 'พฤติกรรมที่ต้องเฝ้าระวัง'}
      </h3>
      <div className="space-y-4">
        {categories.map((cat, cIdx) => (
          <div key={cIdx} className="bg-white/80 p-5 rounded-3xl shadow-sm">
            <p className="font-bold text-slate-700 mb-3 text-sm">{cat.cat}</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {cat.items.map((item, iIdx) => {
                const isChecked = selections[type].includes(item);
                return (
                  <label key={iIdx} className={`flex items-start p-3 rounded-2xl border-2 cursor-pointer transition-all ${isChecked ? colorTheme.activeItem : 'bg-white border-transparent hover:bg-slate-50'}`}>
                    <input type="checkbox" className={`mt-0.5 w-5 h-5 rounded border-slate-300 focus:ring-0 cursor-pointer ${colorTheme.checkbox}`} checked={isChecked} onChange={() => toggleSelection(type, item)} />
                    <span className={`ml-3 text-sm leading-tight ${isChecked ? 'font-bold text-slate-800' : 'text-slate-600 font-medium'}`}>{item}</span>
                  </label>
                )
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="bg-white p-6 md:p-8 rounded-[2.5rem] shadow-xl shadow-slate-200/40 border border-slate-100 mt-6 animate-in fade-in slide-in-from-top-4 duration-300">
      <div className="mb-8">
        <h3 className="text-2xl font-black text-slate-800">
          {initialData ? '✏️ แก้ไขแบบประเมินพฤติกรรม' : 'แบบประเมินพฤติกรรม'}
        </h3>
        <p className="text-slate-500 text-sm mt-1 mb-4">เลือกติ๊กพฤติกรรมที่สังเกตเห็นในตัวนักเรียน</p>

        {st5History && st5History.length > 0 && (
          <div className="bg-slate-50 p-4 rounded-2xl border border-slate-100 flex flex-col gap-2">
             <label className="text-sm font-bold text-slate-700">อ้างอิงจากการประเมินสุขภาพจิต (ST-5)</label>
             <select 
               className="w-full md:w-1/2 p-3 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent bg-white text-slate-700 font-medium"
               value={st5RoundId}
               onChange={(e) => {
                 const selectedId = e.target.value;
                 if (selectedId) {
                   const alreadyAssessed = behaviorHistory.find(b => b.st5RoundId === selectedId && (!initialData || b.id !== initialData.id));
                   if (alreadyAssessed) {
                     if (triggerAlert) {
                       triggerAlert('มีการประเมินพฤติกรรมแล้วในครั้งนี้ หากต้องการแก้ไขกรุณากดปุ่ม "แก้ไข" ในรายการด้านล่าง', 'error');
                     }
                     return;
                   }
                 }
                 setSt5RoundId(selectedId);
               }}
             >
                <option value="">ไม่ระบุ / ประเมินทั่วไป</option>
                {st5History.map((st5, idx) => {
                  const roundNum = st5History.length - idx;
                  const dateStr = new Date(st5.timestamp).toLocaleDateString('th-TH', { dateStyle: 'short' });
                  return (
                    <option key={st5.id} value={st5.id}>
                      ครั้งที่ {roundNum} ({dateStr}) - {st5.level || calculateST5(st5.score).level}
                    </option>
                  );
                })}
             </select>
          </div>
        )}
      </div>
      {renderSection('desirable', behaviors.desirable, { bg: 'bg-teal-50/50', border: 'border-teal-100', text: 'text-teal-700', activeItem: 'bg-teal-50 border-teal-200 shadow-sm', checkbox: 'text-teal-500' })}
      {renderSection('undesirable', behaviors.undesirable, { bg: 'bg-rose-50/50', border: 'border-rose-100', text: 'text-rose-700', activeItem: 'bg-rose-50 border-rose-200 shadow-sm', checkbox: 'text-rose-500' })}
      
      <div className="flex flex-col-reverse md:flex-row gap-4 mt-8 pt-6">
        <button onClick={onDone} className="flex-1 py-4 bg-slate-100 rounded-2xl text-slate-500 font-bold hover:bg-slate-200 transition">ยกเลิก</button>
        <button onClick={handleSave} className="flex-[2] py-4 bg-slate-800 text-white rounded-2xl font-bold hover:bg-slate-700 shadow-lg transition">
          {initialData ? 'บันทึกการแก้ไข' : 'บันทึกพฤติกรรม'}
        </button>
      </div>
    </div>
  );
}
