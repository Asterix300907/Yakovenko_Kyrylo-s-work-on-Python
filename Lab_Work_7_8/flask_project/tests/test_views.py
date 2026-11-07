import pytest
from models import Author, Post, Tag, post_tags
from app import db

@pytest.fixture
def sample_post(app):
    with app.app_context():
        author = Author(name='Автор', email='a@t.com')
        db.session.add(author)
        db.session.commit()
        post = Post(
            title='Тестова стаття',
            slug='test-post',
            author_id=author.id,
            content='Контент',
            status='published'
        )
        db.session.add(post)
        db.session.commit()
        return post

def test_index_200(client):
    """Позитивний: головна сторінка — 200."""
    response = client.get('/')
    assert response.status_code == 200
    assert 'Блог на Flask' in response.data.decode('utf-8')

def test_api_posts_200(client, sample_post):
    """Позитивний: API повертає список статей — 200."""
    response = client.get('/api/posts')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['title'] == 'Тестова стаття'

def test_api_posts_empty(client):
    """Граничний: порожня база — повертає []."""
    response = client.get('/api/posts')
    assert response.status_code == 200
    data = response.get_json()
    assert data == []

def test_nonexistent_route_404(client):
    """Негативний: неіснуючий маршрут — 404."""
    response = client.get('/nonexistent')
    assert response.status_code == 404