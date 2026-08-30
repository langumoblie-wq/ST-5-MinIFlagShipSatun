import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

edit_user_start = """  const [formData, setFormData] = useState({
    name: user.name || '',
    accountType: user.accountType || 'student',
    affiliation: user.affiliation || '',
    status: user.status || 'approved',
    password: user.password || ''
  });"""

edit_user_new = """  const [formData, setFormData] = useState({
    name: user.name || '',
    accountType: user.accountType || 'student',
    affiliation: user.affiliation || '',
    status: user.status || 'approved',
    password: user.password || '',
    gender: user.gender || '',
    age: user.age || ''
  });"""

content = content.replace(edit_user_start, edit_user_new)

edit_user_inputs = """          <div>
            <label className={labelClass}>รหัสผ่าน</label>
            <input type="text" className={inputClass} value={formData.password} onChange={e => setFormData({...formData, password: e.target.value})} placeholder="กำหนดรหัสผ่านใหม่" />
          </div>"""

edit_user_inputs_new = """          <div>
            <label className={labelClass}>รหัสผ่าน</label>
            <input type="text" className={inputClass} value={formData.password} onChange={e => setFormData({...formData, password: e.target.value})} placeholder="กำหนดรหัสผ่านใหม่" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className={labelClass}>เพศ</label>
              <select className={inputClass} value={formData.gender} onChange={e => setFormData({...formData, gender: e.target.value})}>
                <option value="">ไม่ระบุ</option>
                <option value="ชาย">ชาย</option>
                <option value="หญิง">หญิง</option>
                <option value="อื่นๆ">อื่นๆ</option>
              </select>
            </div>
            <div>
              <label className={labelClass}>อายุ (ปี)</label>
              <input type="number" className={inputClass} value={formData.age} onChange={e => setFormData({...formData, age: e.target.value})} placeholder="เช่น 15" />
            </div>
          </div>"""

content = content.replace(edit_user_inputs, edit_user_inputs_new)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
