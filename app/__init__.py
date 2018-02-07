from app.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login' # forces user to login before they can see certain page

from app import routes, models, errors
<<<<<<< HEAD

=======
>>>>>>> 72728f7eee4ee9e09ccb82f21e238adaf8439593
