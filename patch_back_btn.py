import re

with open('src/App.tsx', 'r') as f:
    code = f.read()

old_code = """<button onClick={onBack} className="text-slate-400 hover:text-purple-600 mb-2 flex items-center gap-2 font-bold transition bg-white px-4 py-2 rounded-full shadow-sm border border-slate-100 w-fit text-sm">"""
new_code = """<button onClick={onBack} className="lg:hidden text-slate-400 hover:text-purple-600 mb-2 flex items-center gap-2 font-bold transition bg-white px-4 py-2 rounded-full shadow-sm border border-slate-100 w-fit text-sm">"""

if old_code in code:
    code = code.replace(old_code, new_code)
    with open('src/App.tsx', 'w') as f:
        f.write(code)
    print("Patched back button")
else:
    print("Could not find back button")
