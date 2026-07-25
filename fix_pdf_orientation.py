import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

start_str = "function ProjectReportDashboard("
end_str = "function ST5Form("
parts = content.split(start_str)
if len(parts) > 1:
    body = parts[1].split(end_str)[0]
    
    # Update orientation
    body = body.replace("const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });", "const pdf = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' });")
    
    # Update font family
    body = body.replace('className="bg-white p-12 w-[1122px] font-sans"', 'className="bg-white p-12 w-[1122px]" style={{ fontFamily: "Kanit, sans-serif" }}')
    
    new_content = parts[0] + start_str + body + end_str + parts[1].split(end_str)[1]
    with open('src/App.tsx', 'w') as f:
        f.write(new_content)
    print("Fixed orientation and font")
else:
    print("Could not find ProjectReportDashboard")
