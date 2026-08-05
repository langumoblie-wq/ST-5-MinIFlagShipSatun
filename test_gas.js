const url = "https://script.google.com/macros/s/AKfycbwyPyksvhRl8wwGniD99SMtQFe7BnSU3w-pgJaIopomxxoM9xMFyFTidZAnsg32nHuk/exec";
fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'text/plain;charset=utf-8' },
  body: JSON.stringify({ action: 'GET', sheetName: 'Users' })
}).then(res => res.text()).then(text => {
  console.log("RESPONSE:", text);
}).catch(err => {
  console.log("ERROR:", err);
});
