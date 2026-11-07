import pytest
from app import app as flask_app, db

@pytest.fixture(scope="function")
def app():
    """Фікстура для створення тестового додатка з БД в пам'яті."""
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Тестовий клієнт Flask."""
    return app.test_client()