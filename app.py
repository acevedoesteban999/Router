from flask import Flask, send_from_directory, jsonify, request ,render_template , redirect ,url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash
from ping import api_bp

app = Flask(__name__, static_url_path='', static_folder='./static')

app.config['SECRET_KEY'] = 'test12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class AddUserForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Guardar')

@app.route('/')
def root():
    try:
        users_db = User.query.all()
        users = [{'id': u.id, 'username': u.username} for u in users_db]
    except:
        users = []
    return render_template('index.html', users = users)

@app.route('/login', methods=['POST'])
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
        driver.find_element(By.ID, "username").send_keys(user.username)
        driver.find_element(By.ID, "password").send_keys(user.password)
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


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        db.session.add(User(username=form.username.data, password=form.password.data))
        db.session.commit()
        return redirect('/')
    return render_template('add_user.html', form=form)






with app.app_context():
    db.create_all()
    
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)