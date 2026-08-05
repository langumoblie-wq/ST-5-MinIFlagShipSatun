const GAS_URL = "https://script.google.com/macros/s/AKfycbwyPyksvhRl8wwGniD99SMtQFe7BnSU3w-pgJaIopomxxoM9xMFyFTidZAnsg32nHuk/exec";

const run = async () => {
  const payload = { action: 'GET', sheetName: 'Users', data: {} };
  
  const response = await fetch(GAS_URL, {
    method: 'POST',
    body: JSON.stringify(payload)
  });
  
  const text = await response.text();
  console.log("Raw Text:", text.substring(0, 100));
};
run();
