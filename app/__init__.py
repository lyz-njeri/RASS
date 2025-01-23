from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes import auth, main, agreements, rooms
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(agreements.bp)
    app.register_blueprint(rooms.bp)

    return app