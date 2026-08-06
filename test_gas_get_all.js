const GAS_URL = "https://script.google.com/macros/s/AKfycbwyPyksvhRl8wwGniD99SMtQFe7BnSU3w-pgJaIopomxxoM9xMFyFTidZAnsg32nHuk/exec";
const run = async () => {
  const sheets = ['Users', 'ST5', 'Behaviors', 'Settings'];
  for (const sheet of sheets) {
      try {
          const response = await fetch(GAS_URL, {
              method: 'POST',
              headers: {
                'Content-Type': 'text/plain;charset=utf-8'
              },
              body: JSON.stringify({ action: 'GET', sheetName: sheet })
          });
          const text = await response.text();
          console.log(`Sheet ${sheet}:`, text);
      } catch(e) {
          console.log(`Error ${sheet}:`, e);
      }
  }
};
run();
