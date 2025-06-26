from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_cors import CORS
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
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
CORS(app)
mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

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
        admin = User(email='estagioparceiro@gmail.com', senha=os.getenv('ADMIN_PASSWORD'), role=RoleEnum.ADMIN)
        db.session.add(admin)
        db.session.commit()
        # print("Admin criado")