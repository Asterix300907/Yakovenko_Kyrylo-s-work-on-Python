"""Тести для REST API."""

import pytest
import json
from app import app, db
from models import Book


def test_api_get_books(client, sample_books):
    """Тест отримання списку книг через API."""
    response = client.get('/api/books')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    # Перевіряємо, що наші 3 книги є в базі (може бути >= 3, якщо app.py додав свої)
    assert len(data) >= 3
    # Перевіряємо, що перша книга саме наша
    assert any(book['title'] == 'Python для початківців' for book in data)


def test_api_get_book(client, sample_books):
    """Тест отримання однієї книги через API."""
    book_id = sample_books[0].id
    response = client.get(f'/api/books/{book_id}')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['title'] == 'Python для початківців'
    assert data['author'] == 'Іван Петренко'


def test_api_get_book_404(client):
    """Тест неіснуючої книги через API."""
    response = client.get('/api/books/999')
    assert response.status_code == 404


def test_api_create_book(client):
    """Тест створення книги через API."""
    new_book = {
        'title': 'Нова книга',
        'author': 'Новий Автор',
        'genre': 'Тест',
        'price': 200,
        'stock': 10,
        'isbn': '978-999'
    }
    
    response = client.post('/api/books', 
                          data=json.dumps(new_book),
                          content_type='application/json')
    
    assert response.status_code == 201
    
    data = json.loads(response.data)
    assert data['title'] == 'Нова книга'
    assert data['price'] == 200


def test_api_update_book(client, sample_books):
    """Тест оновлення книги через API."""
    book_id = sample_books[0].id
    updated_data = {
        'title': 'Оновлена назва',
        'author': 'Новий Автор',
        'genre': 'Новий жанр',
        'price': 500,
        'stock': 15
    }
    
    response = client.put(f'/api/books/{book_id}',
                         data=json.dumps(updated_data),
                         content_type='application/json')
    
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['title'] == 'Оновлена назва'
    assert data['price'] == 500


def test_api_delete_book(client, sample_books):
    """Тест видалення книги через API."""
    book_id = sample_books[0].id
    response = client.delete(f'/api/books/{book_id}')
    assert response.status_code == 204
    
    # Перевірити, що книга видалена
    response = client.get(f'/api/books/{book_id}')
    assert response.status_code == 404