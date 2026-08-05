import sys

with open('GAS_API_CODE.gs', 'r') as f:
    content = f.read()

old_code = """             if (headers[i] === 'timestamp' || headers[i] === 'createdAt' || headers[i] === 'updatedAt') {
                 if (typeof val === 'number' || !isNaN(Number(val))) {
                     val = new Date(Number(val));
                 }
             } else if (typeof val === 'object') {"""

new_code = """             if (headers[i] === 'timestamp' || headers[i] === 'createdAt' || headers[i] === 'updatedAt') {
                 if (typeof val === 'number' || (typeof val === 'string' && !isNaN(Number(val)))) {
                     val = new Date(Number(val));
                 } else if (typeof val === 'string') {
                     var pd = new Date(val);
                     if (!isNaN(pd.getTime())) val = pd;
                 }
             } else if (typeof val === 'object') {"""

if old_code in content:
    content = content.replace(old_code, new_code)
    print("Replaced ADD logic 2")

old_code_update = """            if (key === 'timestamp' || key === 'createdAt' || key === 'updatedAt') {
                 if (typeof val === 'number' || !isNaN(Number(val))) {
                     val = new Date(Number(val));
                 }
            } else if (typeof val === 'object') {"""

new_code_update = """            if (key === 'timestamp' || key === 'createdAt' || key === 'updatedAt') {
                 if (typeof val === 'number' || (typeof val === 'string' && !isNaN(Number(val)))) {
                     val = new Date(Number(val));
                 } else if (typeof val === 'string') {
                     var pd = new Date(val);
                     if (!isNaN(pd.getTime())) val = pd;
                 }
            } else if (typeof val === 'object') {"""

if old_code_update in content:
    content = content.replace(old_code_update, new_code_update)
    print("Replaced UPDATE logic 2")

with open('GAS_API_CODE.gs', 'w') as f:
    f.write(content)
