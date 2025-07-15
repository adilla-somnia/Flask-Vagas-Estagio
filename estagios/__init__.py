from flask import Flask, jsonify, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_cors import CORS
from werkzeug.security import generate_password_hash
import os

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['SECRET_KEY'] =  '123456789' ##os.getenv('SECRET_KEY')
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

CORS(app, supports_credentials=True)

mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'auth.login'
@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'mensagem': 'Você precisa estar logado para acessar este recurso.', 'codigo_erro': 401}), 401


from .models import User, RoleEnum 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from .routes.admin import admin_bp
from .routes.empresa import empresa_bp
from .routes.estudante import estudante_bp
from .routes.vaga import vaga_bp
from .routes.candidatura import candidatura_bp
from .routes.auth import auth_bp

app.register_blueprint(admin_bp)
app.register_blueprint(empresa_bp)
app.register_blueprint(estudante_bp)
app.register_blueprint(vaga_bp)
app.register_blueprint(candidatura_bp)
app.register_blueprint(auth_bp)

with app.app_context():
    db.create_all()
    from estagios.models import User, RoleEnum
    if not User.query.filter_by(email='estagioparceiro@gmail.com').first():
        admin = User(email='admin@estagioparceiro.edu.br',
                     senha=generate_password_hash('123456'),
                     role=RoleEnum.ADMIN)
        db.session.add(admin)
        db.session.commit()
        # print("Admin criado")
