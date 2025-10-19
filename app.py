from flask import Flask, send_from_directory, jsonify, request
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

app = Flask(__name__, static_url_path='', static_folder='./static')

@app.route('/')
def root():
    return send_from_directory('./static', 'index.html')

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('user', '').strip()
    pasw = request.form.get('pass', '').strip()
    if not user or not pasw:
        return jsonify(ok=False, error='Faltan datos')

    # Configurar Chrome headless
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    driver_path = '/usr/bin/chromedriver'  # Asegúrate de tener chromedriver instalado

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(15)
        driver.get("https://secure.etecsa.net:8443/")

        # Rellenar formulario
        driver.find_element(By.ID, "username").send_keys(user)
        driver.find_element(By.ID, "password").send_keys(pasw)
        driver.find_element(By.ID, "btnSubmit").click()

        # Esperar redirección o mensaje
        driver.implicitly_wait(5)
        if "portal" in driver.current_url or "bienvenido" in driver.page_source.lower():
            return jsonify(ok=True)
        else:
            return jsonify(ok=False, error='Credenciales inválidas o error en el portal')
    except TimeoutException:
        return jsonify(ok=False, error='Timeout al cargar el portal')
    except Exception as e:
        return jsonify(ok=False, error=str(e))
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)