import sys
import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("getElementById('report-dashboard-container');", "getElementById('pdf-print-container');")

printable_table = """
      {/* Hidden Printable Container for PDF */}
      <div className="absolute top-[-9999px] left-[-9999px]">
        <div id="pdf-print-container" className="bg-white p-12 w-[1122px] font-sans">
            <h1 className="text-xl font-bold text-center mb-6 text-black">สรุปผลและการติดตามคามก้าวหน้าโครงการ Mental Care คัดกรองจิต & ประเมินพฤติกรรม</h1>
            
            <table className="w-full border-collapse border border-black text-sm text-black mb-4">
                <thead>
                    <tr>
                        <th rowSpan={2} className="border border-black p-2 text-center bg-gray-50 align-middle">พื้นที่เป้าหมาย (AREA)</th>
                        <th rowSpan={2} className="border border-black p-2 text-center bg-gray-50 align-middle">โมเดล / อำเภอ</th>
                        <th rowSpan={2} className="border border-black p-2 text-center bg-gray-50 align-middle">เป้าหมาย(คน)</th>
                        <th colSpan={Math.max(...(selectedAffiliation === 'all' ? affiliations : [selectedAffiliation]).map(a => Math.max(...Object.keys(getStats(a).visitsBreakdown).map(Number), 0)), 1) * 2} className="border border-black p-2 text-center bg-gray-50">
                            จำนวนที่ได้รับการคัดกรอง(คน)
                        </th>
                    </tr>
                    <tr>
                        {Array.from({ length: Math.max(...(selectedAffiliation === 'all' ? affiliations : [selectedAffiliation]).map(a => Math.max(...Object.keys(getStats(a).visitsBreakdown).map(Number), 0)), 1) }).map((_, i) => (
                            <React.Fragment key={i}>
                                <th className="border border-black p-2 text-center bg-gray-50">ครั้งที่ {i + 1}</th>
                                <th className="border border-black p-2 text-center bg-gray-50">ร้อยละ</th>
                            </React.Fragment>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {(selectedAffiliation === 'all' ? affiliations : [selectedAffiliation]).map(affil => {
                        const stats = getStats(affil);
                        const maxVisitsOverall = Math.max(...(selectedAffiliation === 'all' ? affiliations : [selectedAffiliation]).map(a => Math.max(...Object.keys(getStats(a).visitsBreakdown).map(Number), 0)), 1);
                        return (
                            <tr key={affil}>
                                <td className="border border-black p-2">{affil}</td>
                                <td className="border border-black p-2 text-center">ตำบล</td>
                                <td className="border border-black p-2 text-center">{stats.target}</td>
                                {Array.from({ length: maxVisitsOverall }).map((_, i) => {
                                    const visitNum = i + 1;
                                    const count = stats.visitsBreakdown[visitNum] || 0;
                                    const percent = stats.target > 0 ? ((count / stats.target) * 100).toFixed(1) : '0.0';
                                    return (
                                        <React.Fragment key={visitNum}>
                                            <td className="border border-black p-2 text-center">{count > 0 ? count : ''}</td>
                                            <td className="border border-black p-2 text-center">{count > 0 ? percent : ''}</td>
                                        </React.Fragment>
                                    );
                                })}
                            </tr>
                        );
                    })}
                </tbody>
            </table>
            
            <div className="mt-4 text-left text-sm italic text-slate-800 font-bold">
                หมายเหตุ ครั้งที่ เพิ่มตามจำนวน ที่พบการคัดกรอง
            </div>
            <div className="mt-1 text-right text-sm italic text-slate-800 font-bold">
                ภายใต้กิจกรรม MiniFlagShip Saun
            </div>
        </div>
      </div>
"""

start_str = "function ProjectReportDashboard("
end_str = "function ST5Form("
parts = content.split(start_str)
if len(parts) > 1:
    body = parts[1].split(end_str)[0]
    
    body_parts = body.rsplit('    </div>\n  );\n}', 1)
    if len(body_parts) == 2:
        new_body = body_parts[0] + printable_table + '\n    </div>\n  );\n}'
        new_content = parts[0] + start_str + new_body + end_str + parts[1].split(end_str)[1]
        
        with open('src/App.tsx', 'w') as f:
            f.write(new_content)
        print("Updated ProjectReportDashboard")
    else:
        print("Could not find end of ProjectReportDashboard")
else:
    print("Could not find ProjectReportDashboard")

