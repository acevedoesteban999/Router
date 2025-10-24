/* ---------- helpers ---------- */
async function ping(host, ms=3000){
  const ctrl = new AbortController();
  const t    = setTimeout(()=>ctrl.abort(), ms);
  try{
    await fetch(`${host}`, {mode:'no-cors', signal:ctrl.signal});
    clearTimeout(t); return true;
  }catch{ clearTimeout(t); return false;}
}

async function updateLed(){
  let color = 'bg-danger';
  let containers = {
    'no-network':'',
    'network':'',
    'router':''
  }
  let form_display = 'd-none'
  const internet = await ping('https://8.8.8.8');
  if(internet){
    containers['network'] = 'bg-success';
  }
  else{
    const portal = await ping('https://secure.etecsa.net:8443');
    if(portal){
      containers['router'] = 'bg-secondary';
      form_display = "d-block"
    }
    else
      containers['no-network'] = 'bg-danger';
    
  }
  Object.entries(containers).forEach(([tag, bgClass]) => {
    let el = document.getElementById(tag)
    el.className = el.className
               .split(' ')
               .filter(c => !c.startsWith('bg-'))
               .join(' ');
    if (bgClass) el.classList.add(bgClass);
  });
  
  document.getElementById('loginForm').className = form_display
  
}

setInterval(updateLed, 5000);
updateLed();


async function loadUsers(){
  const res = await fetch('/api/users');
  const users = await res.json();
  const sel = document.getElementById('userSelect');
  sel.innerHTML = users.map(u => `<option value="${u.id}">${u.username}</option>`).join('');
}
loadUsers();
