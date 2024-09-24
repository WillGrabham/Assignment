import pytest

from app import create_app
from website import db


@pytest.fixture(scope="module")
def app():
    flask_app = create_app()
    flask_app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )
    yield flask_app


@pytest.fixture(scope="module")
def test_client(app):
    testing_client = app.test_client()
    with app.app_context():
        yield testing_client


@pytest.fixture(scope="module")
def init_database(app):
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
