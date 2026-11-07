import pytest
from django.urls import reverse
from blog.models import Author, Post

@pytest.mark.django_db
class TestPostViews:
    
    @pytest.fixture
    def published_post(self):
        author = Author.objects.create(name='Тест', email='t@t.com')
        return Post.objects.create(
            title='Тестова стаття',
            slug='test-post',
            author=author,
            content='Тестовий контент',
            status='published'
        )
    
    @pytest.fixture
    def draft_post(self):
        author = Author.objects.create(name='Тест2', email='t2@t.com')
        return Post.objects.create(
            title='Чернетка',
            slug='draft-post',
            author=author,
            content='Чернетка контент',
            status='draft'
        )
    
    def test_post_list_200(self, client, published_post):
        """Позитивний: список статей повертає 200."""
        response = client.get(reverse('post_list'))
        assert response.status_code == 200
        assert 'Тестова стаття' in response.content.decode()
    
    def test_post_detail_200(self, client, published_post):
        """Позитивний: детальна сторінка існуючої статті — 200."""
        response = client.get(reverse('post_detail', args=['test-post']))
        assert response.status_code == 200
        assert 'Тестовий контент' in response.content.decode()
    
    def test_post_detail_404(self, client):
        """Негативний: неіснуюча стаття — 404."""
        response = client.get(reverse('post_detail', args=['nonexistent']))
        assert response.status_code == 404
    
    def test_draft_not_in_list(self, client, published_post, draft_post):
        """Граничний: чернетка не показується у списку."""
        response = client.get(reverse('post_list'))
        assert 'Тестова стаття' in response.content.decode()
        assert 'Чернетка' not in response.content.decode()