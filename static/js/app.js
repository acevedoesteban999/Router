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
  let container = 'no-network'
  let form_class = 'd-none'
  const internet = await ping('https://8.8.8.8');
  if(internet){
    color = 'bg-success';
    container = 'network'
  }
  else{
    const portal = await ping('https://secure.etecsa.net:8443');
    if(portal){
      color = 'bg-secondary';
      container = 'router';
      form_class = "d-block"
    }
    
  }
  el = document.getElementById(container)
  el.className = el.className
               .split(' ')
               .filter(c => !c.startsWith('bg-'))
               .join(' ');
  el.classList.add(color);
  document.getElementById('loginForm').className = form_class
  
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
