// async function ping(host, ms=3000){
//   const ctrl = new AbortController();
//   const t    = setTimeout(()=>ctrl.abort(), ms);
//   try{
//     await fetch(`${host}`, {mode:'no-cors', signal:ctrl.signal});
//     clearTimeout(t); return true;
//   }catch{ clearTimeout(t); return false;}
// }

// async function updateLed(){
//   let color = 'bg-danger';
//   let containers = {
//     'no-network':'',
//     'network':'',
//     'router':''
//   }
//   let form_display = 'd-none'
//   const internet = await ping('https://8.8.8.8');
//   if(internet){
//     containers['network'] = 'bg-success';
//   }
//   else{
//     const portal = await ping('https://secure.etecsa.net:8443');
//     if(portal){
//       containers['router'] = 'bg-secondary';
//       form_display = "d-block"
//     }
//     else
//       containers['no-network'] = 'bg-danger';
    
//   }
//   Object.entries(containers).forEach(([tag, bgClass]) => {
//     let el = document.getElementById(tag)
//     el.className = el.className
//                .split(' ')
//                .filter(c => !c.startsWith('bg-'))
//                .join(' ');
//     if (bgClass) el.classList.add(bgClass);
//   });
  
//   document.getElementById('loginForm').className = form_display
  
// }

async function updateLed() {
  const { status } = await (await fetch('/api/status')).json();

  const containers = {
    'no-network': '',
    'network':    '',
    'router':     ''
  };

  let formDisplay = 'd-none';

  if (status === 'network') {
    containers.network = 'bg-success';
  } else if (status === 'router') {
    containers.router  = 'bg-secondary';
    formDisplay        = 'd-block';
  } else {
    containers['no-network'] = 'bg-danger';
  }

  Object.entries(containers).forEach(([tag, bgClass]) => {
    const el = document.getElementById(tag);
    if (!el) return;
    el.className = el.className
                   .split(' ')
                   .filter(c => !c.startsWith('bg-'))
                   .join(' ');
    if (bgClass) el.classList.add(bgClass);
  });

  const loginForm = document.getElementById('loginForm');
  if (loginForm) loginForm.className = formDisplay;
}

/* ---------- arrancar y repetir ---------- */
updateLed();
setInterval(updateLed, 5000);

setInterval(updateLed, 5000);
updateLed();




document.getElementById('btnConnect').addEventListener('click', async () => {
  const userId = document.getElementById('userSelect').value;
  if (!userId) { alert('Selecciona un usuario'); return; }
  
  try {
    const res = await fetch('/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({user_id: userId})
    });
    if (res.ok) {
      window.location = "/"
    } else {
      alert('Error al conectar');
    }
  } catch (e) {
    console.error(e);
  }
});