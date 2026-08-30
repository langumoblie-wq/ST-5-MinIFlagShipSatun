import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace editing target state and effects
content = re.sub(r'const \[targets, setTargets\] = useState\(\{\}\);\n\s*const \[globalTarget, setGlobalTarget\] = useState\(1000\);', '', content)
content = re.sub(r'const \[editingTarget, setEditingTarget\] = useState\(null\);', '', content)

load_targets_block = r'useEffect\(\(\) => \{\n\s*const loadTargets = async \(\) => \{[\s\S]*?loadTargets\(\);\n\s*\}, \[\]\);'
content = re.sub(load_targets_block, '', content)

save_targets_block = r'const handleSaveTarget = async \(affil, value\) => \{[\s\S]*?^\s*\};\n'
content = re.sub(save_targets_block, '', content, flags=re.MULTILINE)

# Hardcode target in getStats
content = re.sub(r"const target = affil === 'all' \? globalTarget : \(targets\[affil\] \|\| 100\);", "const target = 50;", content)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
