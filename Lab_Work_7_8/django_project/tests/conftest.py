"""Фікстури для Django тестів."""

import pytest
from blog.models import Author, Profile, Tag, Post, Comment


@pytest.fixture
def author(db):
    """Тестовий автор."""
    return Author.objects.create(
        name='Тест Автор',
        email='test@example.com',
        bio='Тестова біографія'
    )


@pytest.fixture
def profile(author):
    """Тестовий профіль."""
    return Profile.objects.create(
        author=author,
        website='https://test.blog',
        social_media='@testauthor'
    )


@pytest.fixture
def tag(db):
    """Тестовий тег."""
    return Tag.objects.create(name='Python', slug='python')


@pytest.fixture
def post(author, tag):
    """Тестова стаття."""
    post = Post.objects.create(
        title='Тестова стаття',
        slug='test-post',
        author=author,
        content='Тестовий контент статті',
        status='published'
    )
    post.tags.add(tag)
    return post


@pytest.fixture
def comment(post):
    """Тестовий коментар."""
    return Comment.objects.create(
        post=post,
        author_name='Тест Читач',
        author_email='reader@test.com',
        content='Тестовий коментар',
        is_approved=True
    )