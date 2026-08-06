const GAS_URL = "https://script.google.com/macros/s/AKfycbwyPyksvhRl8wwGniD99SMtQFe7BnSU3w-pgJaIopomxxoM9xMFyFTidZAnsg32nHuk/exec";

const run = async () => {
  const response = await fetch(GAS_URL + "?action=sync", {
    method: 'GET'
  });
  
  const text = await response.text();
  console.log("doGet Sync:", text);
};
run();
