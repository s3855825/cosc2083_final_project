from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config


app = Flask(__name__, template_folder='templates', static_folder='templates/assets')
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)
# require users to login
login_manager.login_view = 'login'

# db = session_local()
# models.base.metadata.create_all(bind=engine)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

db.create_all()
