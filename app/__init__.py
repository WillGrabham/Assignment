from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()
app = Flask(__name__)


def create_app():
    app.config.from_object(Config)
    db.init_app(app)
    from app.routes import main
    app.register_blueprint(main)
    return app
