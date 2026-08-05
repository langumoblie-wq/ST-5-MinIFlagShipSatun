import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

old_code = """      const parts = StringDate.split(' ');
      if (parts.length >= 2) {
         const [d, t] = parts;
         const [day, mo, yr] = d.split('/');
         const [h, m, s] = t.split(':');
         return new Date(Number(yr), Number(mo)-1, Number(day), Number(h), Number(m), Number(s)).getTime();
      }"""

new_code = """      const parts = StringDate.split(' ');
      if (parts.length >= 2 && StringDate.includes('/')) {
         const [d, t] = parts;
         const [day, mo, yr] = (d || '').split('/');
         const [h, m, s] = (t || '').split(':');
         const pd = new Date(Number(yr), Number(mo)-1, Number(day), Number(h) || 0, Number(m) || 0, Number(s) || 0).getTime();
         if (!isNaN(pd)) return pd;
      }"""

if old_code in content:
    content = content.replace(old_code, new_code)
    print("Replaced parseSheetDate logic")

with open('src/App.tsx', 'w') as f:
    f.write(content)
