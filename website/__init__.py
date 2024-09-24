from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from website.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "main.tutor_login"
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.register_error_handler(404, not_found)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from website.routes import main

    app.register_blueprint(main)
    return app


def not_found(error):
    return render_template("not_found.html"), 404
