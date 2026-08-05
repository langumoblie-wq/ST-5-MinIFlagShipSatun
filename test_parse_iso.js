const parseSheetDate = (dateStr) => {
  if(!dateStr) return Date.now();
  try {
      if (typeof dateStr === 'number') return dateStr;
      const StringDate = String(dateStr);
      const parts = StringDate.split(' ');
      if (parts.length >= 2 && StringDate.includes('/')) {
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

console.log("Parsed result:", parseSheetDate("2026-08-05T04:42:43.322Z"));
console.log("Parsed result for legacy:", parseSheetDate("05/08/2569 04:42:43"));
