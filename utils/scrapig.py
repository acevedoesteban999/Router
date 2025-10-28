import os
from flask import Blueprint,jsonify,request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import TimeoutException
from .models import User

api_selenium = Blueprint('selenium', __name__)

@api_selenium.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    user_id_form = str(data.get('user_id', '')).strip()
    if not user_id_form:
        return jsonify(ok=False, error='No User in Request')

    try:
        user_id = int(user_id_form)
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify(ok=False, error='Usuario no encontrado')
    except ValueError:
        return jsonify(ok=False, error='ID inválido')
    
    firefox_driver_path = os.getenv('FIREFOX_DRIVER_PATH')
    gecodriver_path = os.getenv('GECODRIVER_PATH')
    sandbox = os.getenv('SANDBOX')
    options = Options()
    if not sandbox:
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.binary_location = firefox_driver_path
    try:
        service = Service(executable_path=gecodriver_path)
        driver  = webdriver.Firefox(service=service, options=options)
        
        driver.set_page_load_timeout(15)
        driver.get("https://secure.etecsa.net:8443/")

        
        driver.find_element(By.ID, "username").send_keys(user.username)
        driver.find_element(By.ID, "password").send_keys(user.password)
        # driver.find_element(By.ID, "btnSubmit").click()

        # driver.implicitly_wait(5)
        # if "portal" in driver.current_url or "bienvenido" in driver.page_source.lower():
            # return jsonify(ok=True)
        # else:
            # return jsonify(ok=False, error='Credenciales inválidas o error en el portal')
    except TimeoutException:
        return jsonify(ok=False, error='Timeout al cargar el portal')
    except Exception as e:
        return jsonify(ok=False, error=str(e))
    finally:
        driver.quit()