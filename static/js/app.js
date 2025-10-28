
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


updateLed();
setInterval(updateLed, 5000);





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