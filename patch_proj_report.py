import sys
import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace uniqueScreenedCount logic in ProjectReportDashboard
old_logic = """    const behaviorRepeatScreenedStudents = studentsInAffil
        .filter(u => (behaviorUserVisits[u.id]?.length || 0) > 1)
        .map(u => ({
            ...u,
            times: behaviorUserVisits[u.id].length,
            visits: behaviorUserVisits[u.id].sort((a,b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
        }))
        .sort((a, b) => b.times - a.times);

    // Backward compatibility for table (we could use st5 unique count as total unique)
    const target = affil === 'all' ? globalTarget : (targets[affil] || 100);
    const progressPercent = target > 0 ? ((st5UniqueScreenedCount / target) * 100).toFixed(1) : 0;

    // We will keep visitsBreakdown mapped to st5VisitsBreakdown to not break the PDF code temporarily,
    // although PDF may also need an update if they want to see behavior data. 
    // Wait, the PDF already uses visitsBreakdown for ST-5.
    
    return {
        uniqueScreenedCount: st5UniqueScreenedCount,
        totalVisitsCount: st5TotalVisitsCount,"""

new_logic = """    const behaviorRepeatScreenedStudents = studentsInAffil
        .filter(u => (behaviorUserVisits[u.id]?.length || 0) > 1)
        .map(u => ({
            ...u,
            times: behaviorUserVisits[u.id].length,
            visits: behaviorUserVisits[u.id].sort((a,b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
        }))
        .sort((a, b) => b.times - a.times);
        
    // Calculate overall unique screened across both ST-5 and Behavior
    const overallUniqueUsers = new Set([...Object.keys(st5UserVisits), ...Object.keys(behaviorUserVisits)]);
    const overallUniqueScreenedCount = overallUniqueUsers.size;

    const target = affil === 'all' ? globalTarget : (targets[affil] || 100);
    const progressPercent = target > 0 ? ((overallUniqueScreenedCount / target) * 100).toFixed(1) : 0;
    
    return {
        uniqueScreenedCount: overallUniqueScreenedCount,
        totalVisitsCount: st5TotalVisitsCount + behaviorTotalVisitsCount,"""

content = content.replace(old_logic, new_logic)

# Replace <Users size={14} /> คัดกรองแล้ว
old_screened = '<Users size={14} /> คัดกรองแล้ว'
new_screened = '<Users size={14} /> ยอดคัดกรอง'
content = content.replace(old_screened, new_screened)

# Add description
old_pbar = '          <div className="h-4 w-full bg-slate-100 rounded-full overflow-hidden border border-slate-200">\n            <div className={`h-full ${parseFloat(overviewStats.progressPercent) >= 100 ? \'bg-emerald-400\' : \'bg-blue-400\'} transition-all duration-1000 relative`}'
new_pbar = '          <p className="text-xs text-slate-500 mb-2">แถบแสดงความคืบหน้าการทำงานเทียบกับเป้าหมายรวม (ยอดผู้ถูกคัดกรองทั้งหมด / เป้าหมาย)</p>\n          <div className="h-4 w-full bg-slate-100 rounded-full overflow-hidden border border-slate-200">\n            <div className={`h-full ${parseFloat(overviewStats.progressPercent) >= 100 ? \'bg-emerald-400\' : \'bg-blue-400\'} transition-all duration-1000 relative`}'
content = content.replace(old_pbar, new_pbar)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
