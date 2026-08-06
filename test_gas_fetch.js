const GAS_URL = "https://script.google.com/macros/s/AKfycbwyPyksvhRl8wwGniD99SMtQFe7BnSU3w-pgJaIopomxxoM9xMFyFTidZAnsg32nHuk/exec";

const run = async () => {
  const response = await fetch(GAS_URL + "?action=sync");
  const data = await response.json();
  console.log("Users count:", data.users?.length);
  console.log("ST5 count:", data.st5?.length);
  console.log("Behaviors count:", data.behaviors?.length);
};
run();
