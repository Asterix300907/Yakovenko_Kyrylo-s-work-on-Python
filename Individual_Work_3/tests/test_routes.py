"""Тести для веб-маршрутів."""

import pytest
from app import app, db
from models import Book


def test_index_page(client, sample_books):
    """Тест головної сторінки."""
    response = client.get('/')
    assert response.status_code == 200
    assert 'Онлайн-Книгарня' in response.data.decode('utf-8')


def test_books_page(client, sample_books):
    """Тест сторінки каталогу."""
    response = client.get('/books')
    assert response.status_code == 200
    assert 'Python для початківців' in response.data.decode('utf-8')


def test_book_detail_page(client, sample_books):
    """Тест сторінки деталей книги."""
    book_id = sample_books[0].id
    response = client.get(f'/books/{book_id}')
    assert response.status_code == 200
    assert 'Python для початківців' in response.data.decode('utf-8')


def test_book_detail_404(client):
    """Тест неіснуючої книги."""
    response = client.get('/books/999')
    assert response.status_code == 404


def test_add_to_cart(client, sample_books):
    """Тест додавання книги до кошика."""
    book_id = sample_books[0].id
    response = client.post(f'/cart/add/{book_id}', follow_redirects=True)
    assert response.status_code == 200
    assert 'додано до кошика' in response.data.decode('utf-8')
    
    with client.session_transaction() as sess:
        assert 'cart' in sess
        assert str(book_id) in sess['cart']


def test_view_cart(client, sample_books):
    """Тест перегляду кошика."""
    book_id = sample_books[0].id
    client.post(f'/cart/add/{book_id}')
    
    response = client.get('/cart')
    assert response.status_code == 200
    assert 'Ваш кошик' in response.data.decode('utf-8')


def test_clear_cart(client, sample_books):
    """Тест очищення кошика."""
    book_id = sample_books[0].id
    client.post(f'/cart/add/{book_id}')
    
    response = client.get('/cart/clear', follow_redirects=True)
    assert response.status_code == 200
    
    with client.session_transaction() as sess:
        assert 'cart' not in sess or len(sess['cart']) == 0


def test_create_order(client, sample_books):
    """Тест оформлення замовлення."""
    book_id = sample_books[0].id
    client.post(f'/cart/add/{book_id}')
    
    response = client.post('/order', data={
        'name': 'Тест Користувач',
        'email': 'test@example.com'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert 'успішно оформлено' in response.data.decode('utf-8')


def test_set_theme_cookie(client):
    """Тест встановлення теми через cookie."""
    response = client.get('/set-theme/dark')
    assert response.status_code == 302
    
    # Перевірити cookie у заголовках редиректу
    assert 'theme' in response.headers.get('Set-Cookie', '')