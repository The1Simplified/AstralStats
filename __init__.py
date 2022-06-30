from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from routes.main.routes import main
    from routes.errors.handlers import errors
    from routes.xbox.routes import xbox
    from routes.playstation.routes import playstation
    from routes.steam.routes import steam
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(xbox)
    app.register_blueprint(playstation)
    app.register_blueprint(steam)

    return app