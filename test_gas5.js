const url = "https://script.google.com/macros/s/AKfycbwyPyksvhRl8wwGniD99SMtQFe7BnSU3w-pgJaIopomxxoM9xMFyFTidZAnsg32nHuk/exec";
fetch(url + "?action=sync", {
  method: 'GET'
}).then(res => res.text()).then(text => console.log(text));
