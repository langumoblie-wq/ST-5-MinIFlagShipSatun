with open('src/App.tsx', 'r') as f:
    content = f.read()

target = """               </button>
            )}"""

replacement = """               </button>
               </>
            )}"""

# Replace only the first occurrence after the line containing "Sparkles size={20}"
parts = content.split("<span>รายงานวิเคราะห์ข้อมูล</span>")
if len(parts) == 2:
    parts[1] = parts[1].replace(target, replacement, 1)
    content = "<span>รายงานวิเคราะห์ข้อมูล</span>".join(parts)
    with open('src/App.tsx', 'w') as f:
        f.write(content)
    print("Fixed")
else:
    print("Not found")
