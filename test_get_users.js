const GAS_URL = "https://script.google.com/macros/s/AKfycbwyPyksvhRl8wwGniD99SMtQFe7BnSU3w-pgJaIopomxxoM9xMFyFTidZAnsg32nHuk/exec";

const gasRequest = async (action, sheetName, data = null) => {
  const payload = { action, sheetName, data };
  
  const response = await fetch(GAS_URL, {
    method: 'POST',
    body: JSON.stringify(payload)
  });
  
  const result = await response.json();
  console.log("Result:", result);
};

gasRequest('GET', 'Users');
