import pytest
from sqlalchemy.exc import IntegrityError
from models import Author, Profile, Tag, Post, Comment, post_tags
from app import db

def test_create_author(app):
    """Тест 1: Створення автора."""
    with app.app_context():
        author = Author(name='Тест Автор', email='test@example.com', bio='Тест')
        db.session.add(author)
        db.session.commit()
        assert author.name == 'Тест Автор'
        assert author.id is not None

def test_author_unique_email(app):
    """Тест 2: Перевірка унікальності email."""
    with app.app_context():
        author = Author(name='Автор 1', email='unique@test.com')
        db.session.add(author)
        db.session.commit()
        with pytest.raises(IntegrityError):
            db.session.add(Author(name='Автор 2', email='unique@test.com'))
            db.session.commit()

def test_profile_one_to_one(app):
    """Тест 3: Перевірка OneToOne зв'язку (Profile)."""
    with app.app_context():
        author = Author(name='Автор для профілю', email='prof@test.com')
        db.session.add(author)
        db.session.commit()
        db.session.add(Profile(author_id=author.id, website='https://first.blog'))
        db.session.commit()
        with pytest.raises(IntegrityError):
            db.session.add(Profile(author_id=author.id, website='https://second.blog'))
            db.session.commit()

def test_post_tags_many_to_many(app):
    """Тест 4: Перевірка ManyToMany зв'язку (Post <-> Tag)."""
    with app.app_context():
        author = Author(name='Автор посту', email='post@test.com')
        db.session.add(author)
        db.session.commit()
        tag = Tag(name='Python', slug='python')
        db.session.add(tag)
        db.session.commit()
        post = Post(title='Тестова стаття', slug='test-post', author_id=author.id, content='Тестовий контент', status='published')
        db.session.add(post)
        db.session.flush()
        db.session.execute(post_tags.insert().values(post_id=post.id, tag_id=tag.id))
        db.session.commit()
        fresh_post = db.session.get(Post, post.id)
        assert tag.id in [t.id for t in fresh_post.tags]

def test_cascade_delete_post(app):
    """Тест 5: Перевірка каскадного видалення коментарів."""
    with app.app_context():
        author = Author(name='Автор для видалення', email='del@test.com')
        db.session.add(author)
        db.session.commit()
        post = Post(title='Стаття для видалення', slug='del-post', author_id=author.id, content='Текст', status='published')
        db.session.add(post)
        db.session.commit()
        comment = Comment(post_id=post.id, author_name='Тест', author_email='t@t.com', content='Тест', is_approved=True)
        db.session.add(comment)
        db.session.commit()
        
        post_id = post.id
        comment_id = comment.id
        
        post_to_delete = db.session.get(Post, post_id)
        db.session.delete(post_to_delete)
        db.session.commit()
        
        assert db.session.get(Post, post_id) is None
        assert db.session.get(Comment, comment_id) is None

@pytest.mark.parametrize('status,expected_count', [
    ('published', 2),
    ('draft', 1),
])
def test_post_status_filter(app, status, expected_count):
    """Тест 6: Параметризований тест фільтрації статей за статусом."""
    with app.app_context():
        auth = Author(name='Параметр Автор', email='param@test.com')
        db.session.add(auth)
        db.session.commit()
        db.session.add_all([
            Post(title='Опубл 1', slug='p1', author_id=auth.id, content='Текст', status='published'),
            Post(title='Опубл 2', slug='p2', author_id=auth.id, content='Текст', status='published'),
            Post(title='Чернетка', slug='d1', author_id=auth.id, content='Текст', status='draft'),
        ])
        db.session.commit()
        count = Post.query.filter_by(status=status).count()
        assert count == expected_count