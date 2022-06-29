from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

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