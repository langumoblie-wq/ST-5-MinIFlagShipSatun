import sys

with open('GAS_API_CODE.gs', 'r') as f:
    content = f.read()

old_code = """        for (var i = 0; i < headers.length; i++) {
          var val = data[headers[i]];
          rowData.push(val !== undefined ? (typeof val === 'object' ? JSON.stringify(val) : val) : "");
        }"""

new_code = """        for (var i = 0; i < headers.length; i++) {
          var val = data[headers[i]];
          if (val !== undefined) {
             if (headers[i] === 'timestamp' || headers[i] === 'createdAt' || headers[i] === 'updatedAt') {
                 if (typeof val === 'number' || !isNaN(Number(val))) {
                     val = new Date(Number(val));
                 }
             } else if (typeof val === 'object') {
                 val = JSON.stringify(val);
             }
             rowData.push(val);
          } else {
             rowData.push("");
          }
        }"""

if old_code in content:
    content = content.replace(old_code, new_code)
    print("Replaced ADD logic")

old_code_update = """        for (var key in data) {
          var colIndex = headers.indexOf(key);
          if (colIndex !== -1) {
            var val = data[key];
            sheet.getRange(foundRow, colIndex + 1).setValue(typeof val === 'object' ? JSON.stringify(val) : val);
          }
        }"""

new_code_update = """        for (var key in data) {
          var colIndex = headers.indexOf(key);
          if (colIndex !== -1) {
            var val = data[key];
            if (key === 'timestamp' || key === 'createdAt' || key === 'updatedAt') {
                 if (typeof val === 'number' || !isNaN(Number(val))) {
                     val = new Date(Number(val));
                 }
            } else if (typeof val === 'object') {
                val = JSON.stringify(val);
            }
            sheet.getRange(foundRow, colIndex + 1).setValue(val);
          }
        }"""

if old_code_update in content:
    content = content.replace(old_code_update, new_code_update)
    print("Replaced UPDATE logic")

with open('GAS_API_CODE.gs', 'w') as f:
    f.write(content)
