"""Фікстури для тестів."""

import pytest
from app import app, db
from models import Book, Order, OrderItem


@pytest.fixture
def client():
    """Тестовий клієнт Flask з чистою базою даних у пам'яті."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.drop_all() 
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


@pytest.fixture
def sample_books(client):
    """Створити тестові книги.
    Працює всередині активного контексту фікстури 'client', 
    тому об'єкти залишаються прив'язаними до сесії і не стають 'detached'.
    """
    books = [
        Book(title='Python для початківців', author='Іван Петренко', 
             genre='Програмування', price=450, stock=10, isbn='978-111'),
        Book(title='Django в дії', author='Марія Сидоренко', 
             genre='Програмування', price=650, stock=5, isbn='978-222'),
        Book(title='Машинне навчання', author='Анна Бондар', 
             genre='Data Science', price=850, stock=7, isbn='978-333'),
    ]
    db.session.add_all(books)
    db.session.commit()
    
    # Використовуємо yield, щоб тримати контекст активним під час тесту
    yield books