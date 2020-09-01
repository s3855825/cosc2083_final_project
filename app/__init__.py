from flask import Flask
from flask_login import LoginManager
from app.database import session_local, engine
from app import models

app = Flask(__name__, template_folder='templates', static_folder='templates/assets')
login = LoginManager(app)
db = session_local()
models.base.metadata.create_all(bind=engine)
