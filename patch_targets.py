import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

old_state = """  const [targets, setTargets] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('project_targets')) || {};
    } catch {
      return {};
    }
  });
  const [globalTarget, setGlobalTarget] = useState(() => {
    return parseInt(localStorage.getItem('project_global_target')) || 1000;
  });
  const [selectedAffiliation, setSelectedAffiliation] = useState('all');
  const [expandedRows, setExpandedRows] = useState({});
  const [editingTarget, setEditingTarget] = useState(null);

  useEffect(() => {
    localStorage.setItem('project_targets', JSON.stringify(targets));
  }, [targets]);

  useEffect(() => {
    localStorage.setItem('project_global_target', globalTarget.toString());
  }, [globalTarget]);"""

new_state = """  const [targets, setTargets] = useState({});
  const [globalTarget, setGlobalTarget] = useState(1000);
  const [selectedAffiliation, setSelectedAffiliation] = useState('all');
  const [expandedRows, setExpandedRows] = useState({});
  const [editingTarget, setEditingTarget] = useState(null);

  useEffect(() => {
    const loadTargets = async () => {
      try {
        const docRef = doc(db, 'artifacts', appId, 'public', 'data', 'settings', 'project_targets');
        const snap = await getDoc(docRef);
        if (snap.exists()) {
          const data = snap.data();
          if (data.targets) {
            try { setTargets(JSON.parse(data.targets)); } catch (e) {}
          }
          if (data.globalTarget) {
            setGlobalTarget(Number(data.globalTarget));
          }
        }
      } catch (err) {
        console.error("Failed to load targets", err);
      }
    };
    loadTargets();
  }, []);"""

content = content.replace(old_state, new_state)

old_save = """  const handleSaveTarget = (affil, value) => {
      if (affil === 'all') {
          setGlobalTarget(Number(value));
      } else {
          setTargets(prev => ({ ...prev, [affil]: Number(value) }));
      }
      setEditingTarget(null);
  };"""

new_save = """  const handleSaveTarget = async (affil, value) => {
      let newGlobal = globalTarget;
      let newTargets = { ...targets };

      if (affil === 'all') {
          newGlobal = Number(value);
          setGlobalTarget(newGlobal);
      } else {
          newTargets[affil] = Number(value);
          setTargets(newTargets);
      }
      setEditingTarget(null);

      try {
         const docRef = doc(db, 'artifacts', appId, 'public', 'data', 'settings', 'project_targets');
         await setDoc(docRef, {
             targets: JSON.stringify(newTargets),
             globalTarget: newGlobal,
             updatedAt: Date.now()
         });
      } catch (err) {
         console.error("Failed to save target", err);
      }
  };"""

content = content.replace(old_save, new_save)

with open('src/App.tsx', 'w') as f:
    f.write(content)
print("Patch applied")
