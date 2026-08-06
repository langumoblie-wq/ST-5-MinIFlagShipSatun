const GAS_URL = "https://script.google.com/macros/s/AKfycbwyPyksvhRl8wwGniD99SMtQFe7BnSU3w-pgJaIopomxxoM9xMFyFTidZAnsg32nHuk/exec";
const run = async () => {
  try {
      const response = await fetch(GAS_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'text/plain;charset=utf-8'
          },
          body: JSON.stringify({ action: 'GET', sheetName: 'Users' })
      });
      const text = await response.text();
      console.log(text);
  } catch(e) {
      console.log("Error:", e);
  }
};
run();
