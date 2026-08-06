const GAS_URL = "https://script.google.com/macros/s/AKfycbwyPyksvhRl8wwGniD99SMtQFe7BnSU3w-pgJaIopomxxoM9xMFyFTidZAnsg32nHuk/exec";
const run = async () => {
  const actions = ['read', 'GET', 'get', 'fetch'];
  for (const action of actions) {
    try {
        const response = await fetch(GAS_URL, {
            method: 'POST',
            body: JSON.stringify({ action, sheetName: 'Users', data: {} })
        });
        console.log(`Action ${action}:`, await response.text());
    } catch(e) {}
  }
};
run();
