"""Тести моделей Django."""

import pytest
from django.db import IntegrityError
from django.db.models import ProtectedError
from blog.models import Author, Profile, Tag, Post, Comment


# === Тести створення та __str__ ===

class TestAuthorModel:
    """Тести моделі Author."""

    def test_create_author(self, author):
        """Тест створення автора."""
        assert author.name == 'Тест Автор'
        assert author.email == 'test@example.com'
        assert author.pk is not None

    def test_author_str(self, author):
        """Тест рядкового представлення."""
        assert str(author) == 'Тест Автор'

    def test_author_unique_email(self, author):
        """Тест унікальності email."""
        with pytest.raises(IntegrityError):
            Author.objects.create(
                name='Інший Автор',
                email='test@example.com'  
            )


class TestProfileModel:
    """Тести моделі Profile."""

    def test_create_profile(self, profile, author):
        """Тест створення профілю."""
        assert profile.author == author
        assert profile.website == 'https://test.blog'

    def test_profile_str(self, profile):
        """Тест рядкового представлення."""
        assert str(profile) == 'Профіль Тест Автор'


class TestTagModel:
    """Тести моделі Tag."""

    def test_create_tag(self, tag):
        """Тест створення тегу."""
        assert tag.name == 'Python'
        assert tag.slug == 'python'

    def test_tag_str(self, tag):
        """Тест рядкового представлення."""
        assert str(tag) == 'Python'


class TestPostModel:
    """Тести моделі Post."""

    def test_create_post(self, post, author):
        """Тест створення статті."""
        assert post.title == 'Тестова стаття'
        assert post.author == author
        assert post.status == 'published'

    def test_post_str(self, post):
        """Тест рядкового представлення."""
        assert str(post) == 'Тестова стаття'

    def test_post_tags_many_to_many(self, post, tag):
        """Тест ManyToMany зв'язку."""
        assert tag in post.tags.all()
        assert post in tag.posts.all()


class TestCommentModel:
    """Тести моделі Comment."""

    def test_create_comment(self, comment, post):
        """Тест створення коментаря."""
        assert comment.post == post
        assert comment.content == 'Тестовий коментар'
        assert comment.is_approved is True

    def test_comment_str(self, comment):
        """Тест рядкового представлення."""
        assert 'Тест Читач' in str(comment)
        assert 'Тестова стаття' in str(comment)

    def test_cascade_delete_post(self, post, comment):
        """Тест каскадного видалення: видалення статті видаляє коментарі."""
        post_id = post.id
        post.delete()
        assert Comment.objects.filter(post_id=post_id).count() == 0


# === Параметризований тест ===

@pytest.mark.parametrize('status,expected_count', [
    ('published', 2),
    ('draft', 1),
    ('published', 2),  # дубль для демонстрації
])
@pytest.mark.django_db
def test_post_status_filter(status, expected_count):
    """Параметризований тест: фільтрація статей за статусом."""
    author = Author.objects.create(name=f'Автор {status}', email=f'{status}@test.com')
    
    # Створити тестові статті
    Post.objects.create(title=f'Опублікована 1', slug=f'pub1-{status}', author=author, status='published')
    Post.objects.create(title=f'Опублікована 2', slug=f'pub2-{status}', author=author, status='published')
    Post.objects.create(title=f'Чернетка', slug=f'draft-{status}', author=author, status='draft')
    
    count = Post.objects.filter(status=status).count()
    assert count == expected_count