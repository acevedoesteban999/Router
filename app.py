from flask import Flask, render_template , redirect , request , jsonify
from utils.models import db,User,AddUserForm
from utils.ping import api_bp
from utils.scrapig import api_selenium
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv() 


def create_app():
    app = Flask(__name__, static_url_path='', static_folder='./static')
    app.config['SECRET_KEY'] = 'test12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    
    db.init_app(app)

   
    app.register_blueprint(api_bp)
    app.register_blueprint(api_selenium)
    
    with app.app_context():
        db.create_all()  

    return app

app = create_app()
CORS(app)

@app.route('/')
def root():
    try:
        users_db = User.query.all()
        users = [{'id': u.id, 'username': u.username} for u in users_db]
    except:
        users = []
    return render_template('index.html', users = users)

@app.route('/get_password', methods=['POST'])
def get_password():
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({'error': 'Falta el campo username'}), 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    return jsonify({'username': user.username, 'password': user.password})


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        db.session.add(User(username=form.username.data, password=form.password.data))
        db.session.commit()
        return redirect('/')
    return render_template('add_user.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)