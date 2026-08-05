const url = "https://script.google.com/macros/s/AKfycbwyPyksvhRl8wwGniD99SMtQFe7BnSU3w-pgJaIopomxxoM9xMFyFTidZAnsg32nHuk/exec";
async function run() {
  const actions = [
    { action: 'GET', sheetName: 'Users' },
    { action: 'TEST', sheetName: 'Users' },
    { action: 'GET', sheetName: 'ST5' },
  ];
  for (const body of actions) {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(body)
    });
    const text = await res.text();
    console.log(body, "->", text);
  }
}
run();
