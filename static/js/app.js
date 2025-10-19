/* ---------- helpers ---------- */
async function ping(host, ms=2000){
  const ctrl = new AbortController();
  const t    = setTimeout(()=>ctrl.abort(), ms);
  try{
    await fetch(`https://${host}/favicon.ico`, {mode:'no-cors', signal:ctrl.signal});
    clearTimeout(t); return true;
  }catch{ clearTimeout(t); return false;}
}

async function updateLed(){
  const internet = await ping('8.8.8.8');
  const portal   = await ping('secure.etecsa.net:8443');
  const led  = document.getElementById('led');
  const form = document.getElementById('loginForm');
  
  let color = 'red';
  
  if(internet)      
    color = 'green';
  else if(portal)   
    color = 'grey';
  
  led.className = color;
  form.style.display = (color==='grey') ? 'block':'none';
}

/* ---------- login ---------- */
async function doLogin(){
  const u = document.getElementById('user').value.trim();
  const p = document.getElementById('pass').value.trim();
  const msg = document.getElementById('msg');
  if(!u||!p){msg.textContent='Complete campos';return;}
  msg.textContent='Conectando...';

  const form = new FormData();
  form.append('user', u);
  form.append('pass', p);

  try{
    const res = await fetch('/login', {method:'POST', body: form});
    const data = await res.json();
    if(data.ok){
      msg.textContent='¡Conectado!';
      setTimeout(()=>location.reload(),1500);
    } else {
      msg.textContent=data.error || 'Error desconocido';
    }
  }catch(e){
    msg.textContent='Error de red';
  }
}

/* ---------- arranque ---------- */
document.getElementById('btnSend').addEventListener('click', doLogin);
setInterval(updateLed, 5000);
updateLed();
