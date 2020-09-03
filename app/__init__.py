import os
from flask import Flask
from flask_login import LoginManager
from app.database import session_local, engine
# from app import models

SECRET_KEY = os.urandom(32)
app = Flask(__name__, template_folder='templates', static_folder='templates/assets')
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
# require users to login
login_manager.login_view = 'login'

db = session_local()
# models.base.metadata.create_all(bind=engine)

