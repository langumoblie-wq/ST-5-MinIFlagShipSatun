const GAS_URL = "https://script.google.com/macros/s/AKfycbwyPyksvhRl8wwGniD99SMtQFe7BnSU3w-pgJaIopomxxoM9xMFyFTidZAnsg32nHuk/exec";
const run = async () => {
  try {
      const response = await fetch(GAS_URL, {
          method: 'POST',
          body: JSON.stringify({ action: 'GET', sheetName: 'Users', data: { createdAt: 1, updatedAt: 1 } })
      });
      const text = await response.text();
      console.log("Response text:", text);
  } catch(e) {
      console.log("Error:", e);
  }
};
run();
