import sys
with open('src/App.tsx', 'r') as f:
    content = f.read()
start_str = "const handlePrint = async () => {"
end_str = "    }, 100);"
parts = content.split(start_str)
if len(parts) > 1:
    body = parts[1].split(end_str)[0]
    print(start_str + body + end_str)
