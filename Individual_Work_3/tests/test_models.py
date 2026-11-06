"""Тести для моделей БД."""

import pytest
from app import app, db
from models import Book, Order, OrderItem


def test_create_book(client):
    """Тест створення книги."""
    with app.app_context():
        book = Book(title='Тестова книга', author='Тест Автор', 
                   genre='Тест', price=100, stock=5, isbn='978-000')
        db.session.add(book)
        db.session.commit()
        
        assert book.id is not None
        assert book.title == 'Тестова книга'
        assert book.price == 100


def test_book_to_dict(client, sample_books):
    """Тест серіалізації книги у dict."""
    with app.app_context():
        book = sample_books[0]
        data = book.to_dict()
        
        assert data['title'] == 'Python для початківців'
        assert data['author'] == 'Іван Петренко'
        assert data['price'] == 450
        assert 'id' in data
        assert 'created_at' in data


def test_create_order(client, sample_books):
    """Тест створення замовлення."""
    with app.app_context():
        order = Order(customer_name='Тест Користувач', 
                     customer_email='test@example.com')
        db.session.add(order)
        db.session.flush()
        
        # Додати елемент замовлення
        item = OrderItem(order_id=order.id, book_id=sample_books[0].id, quantity=2)
        db.session.add(item)
        db.session.commit()
        
        assert order.id is not None
        assert len(order.items) == 1
        assert order.items[0].quantity == 2


def test_order_total_price(client, sample_books):
    """Тест обчислення загальної суми замовлення."""
    with app.app_context():
        order = Order(customer_name='Тест', customer_email='test@test.com')
        db.session.add(order)
        db.session.flush()
        
        # Додати 2 різні книги
        item1 = OrderItem(order_id=order.id, book_id=sample_books[0].id, quantity=2)
        item2 = OrderItem(order_id=order.id, book_id=sample_books[1].id, quantity=1)
        db.session.add_all([item1, item2])
        db.session.commit()
        
        # 2 * 450 + 1 * 650 = 1550
        assert order.total_price() == 1550


def test_book_relationships(client, sample_books):
    """Тест зв'язків між моделями."""
    with app.app_context():
        book = sample_books[0]
        
        # Створити замовлення з цією книгою
        order = Order(customer_name='Тест', customer_email='test@test.com')
        db.session.add(order)
        db.session.flush()
        
        item = OrderItem(order_id=order.id, book_id=book.id, quantity=3)
        db.session.add(item)
        db.session.commit()
        
        # Перевірити зворотний зв'язок
        assert len(book.order_items) == 1
        assert book.order_items[0].quantity == 3