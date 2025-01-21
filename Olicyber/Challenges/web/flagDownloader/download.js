//questa è la funzione che viene utilizzata per scaricre la flag pezzo per pezzo, trovata all'indirizzo: http://flagdownloader.challs.olicyber.it/static/js/download.js
c = document.getElementById('content');

function g(n) {
  fetch(p + n)
    .then((response) => response.json())
    .then((data) => {
      if (data['t']) {
        c.textContent += data['c'];
        setTimeout(() => g(data['n']), data['t']);
      }
    });
}

g(n);
