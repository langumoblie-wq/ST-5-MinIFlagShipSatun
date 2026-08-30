import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace <PieChart width={300}...> and <PieChart> with <RechartsPieChart>
content = re.sub(r'<PieChart\s+width=\{300\}\s+height=\{250\}>', r'<RechartsPieChart width={300} height={250}>', content)
content = re.sub(r'</PieChart>', r'</RechartsPieChart>', content)
content = re.sub(r'<PieChart>', r'<RechartsPieChart>', content)
# Restore the icon PieChart
content = content.replace('<RechartsPieChart size=', '<PieChart size=')
content = content.replace('<RechartsPieChart className=', '<PieChart className=')

# Also fix BarChart in ExecutiveSummaryReport (BarChart2 is the icon, BarChart is recharts)
# Recharts BarChart is imported as BarChart, so it should be fine. Wait, does it conflict?
# No, we only imported BarChart2 and BarChart3 from lucide-react. And BarChart from recharts. So <BarChart> is fine.

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
