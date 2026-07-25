import sys

with open('src/main.tsx', 'r') as f:
    content = f.read()

font_imports = """
import '@fontsource/kanit/300.css';
import '@fontsource/kanit/400.css';
import '@fontsource/kanit/500.css';
import '@fontsource/kanit/600.css';
import '@fontsource/kanit/700.css';
"""

content = content.replace("import './index.css';", "import './index.css';\n" + font_imports)

with open('src/main.tsx', 'w') as f:
    f.write(content)
