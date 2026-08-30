import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_table_logic = """  const renderTable = () => (
        <div className="space-y-4">"""

new_table_logic = """  const renderTable = () => {
        const sortedByRisk = [...tableData].sort((a, b) => b.risk - a.risk);
        const topRiskAffil = sortedByRisk[0];
        const tableInterpretation = topRiskAffil && topRiskAffil.risk > 0 
          ? `การแปรผล: องค์กร/สถานที่ที่มีเยาวชนกลุ่มเสี่ยงสูงสุดคือ "${topRiskAffil.name}" (จำนวน ${topRiskAffil.risk} คน) ควรจัดลำดับความสำคัญในการลงพื้นที่และจัดกิจกรรม Intervention ให้กับสถานที่นี้เป็นอันดับแรก`
          : 'การแปรผล: ปัจจุบันยังไม่พบเยาวชนกลุ่มเสี่ยงในระบบ';
          
        return (
        <div className="space-y-4">"""

content = content.replace(old_table_logic, new_table_logic)

old_table_end = """            </table>
          </div>
        </div>
  );"""

new_table_end = """            </table>
          </div>
          <div className="mt-4 p-4 bg-orange-50/50 rounded-2xl border border-orange-100">
            <p className="text-sm font-medium text-orange-800">{tableInterpretation}</p>
          </div>
        </div>
  );}"""

content = content.replace(old_table_end, new_table_end)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
