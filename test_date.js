const formatDateForSheet = (ts) => {
  if (!ts) return '';
  const d = new Date(ts);
  if (isNaN(d.getTime())) return ts;
  return d.toLocaleString('th-TH', { 
      day: '2-digit', month: '2-digit', year: 'numeric',
      hour: '2-digit', minute: '2-digit', second: '2-digit'
  });
};

const payload = { timestamp: Date.now() };
if (payload.timestamp && typeof payload.timestamp === 'number') {
  payload.timestamp = formatDateForSheet(payload.timestamp);
}
console.log("payload:", payload);
