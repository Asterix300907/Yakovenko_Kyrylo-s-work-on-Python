"""Демонстрація ORM-запитів Flask-SQLAlchemy + транзакції."""

from app import app, db
from models import Author, Profile, Tag, Post, Comment, post_tags


def clear_data():
    """Очистити базу."""
    db.session.execute(post_tags.delete())
    Comment.query.delete()
    Post.query.delete()
    Profile.query.delete()
    Tag.query.delete()
    Author.query.delete()
    db.session.commit()
    print("✅ База очищена\n")


def create_data():
    """CREATE."""
    print("=" * 60)
    print("1. CREATE — створення даних")
    print("=" * 60)

    author1 = Author(name='Іван Петренко', email='ivan@example.com', bio='Досвідчений розробник')
    author2 = Author(name='Марія Сидоренко', email='maria@example.com', bio='Початківець')
    author3 = Author(name='Олексій Коваль', email='alex@example.com', bio='Технічний письменник')
    db.session.add_all([author1, author2, author3])
    db.session.flush()
    print(f"✅ Створено 3 авторів")

    Profile.objects = []  # просто для демонстрації
    db.session.add_all([
        Profile(author_id=author1.id, website='https://ivan.blog'),
        Profile(author_id=author2.id, website='https://maria.blog')
    ])
    print(f"✅ Створено 2 профілі")

    python_tag = Tag(name='Python', slug='python')
    django_tag = Tag(name='Django', slug='django')
    flask_tag = Tag(name='Flask', slug='flask')
    db.session.add_all([python_tag, django_tag, flask_tag])
    db.session.flush()
    print(f"✅ Створено 3 теги")

    post1 = Post(title='Вступ до Python', slug='intro-python', author_id=author1.id, content='Python — це...', status='published')
    post2 = Post(title='Django для початківців', slug='django-beginners', author_id=author1.id, content='Django — це...', status='published')
    post3 = Post(title='Flask vs Django', slug='flask-vs-django', author_id=author3.id, content='Порівняння...', status='published')
    post4 = Post(title='Чернетка статті', slug='draft-post', author_id=author2.id, content='Ще не готово', status='draft')
    db.session.add_all([post1, post2, post3, post4])
    db.session.flush()
    print(f"✅ Створено 4 статті")

    # ManyToMany через проміжну таблицю
    db.session.execute(post_tags.insert().values(post_id=post1.id, tag_id=python_tag.id))
    db.session.execute(post_tags.insert().values(post_id=post1.id, tag_id=django_tag.id))
    db.session.execute(post_tags.insert().values(post_id=post2.id, tag_id=django_tag.id))
    db.session.execute(post_tags.insert().values(post_id=post3.id, tag_id=python_tag.id))
    db.session.execute(post_tags.insert().values(post_id=post3.id, tag_id=flask_tag.id))
    print(f"✅ Теги додано до статей")

    db.session.add_all([
        Comment(post_id=post1.id, author_name='Читач1', author_email='r1@mail.com', content='Чудова стаття!', is_approved=True),
        Comment(post_id=post1.id, author_name='Читач2', author_email='r2@mail.com', content='Дякую!', is_approved=True),
        Comment(post_id=post1.id, author_name='Спам', author_email='spam@mail.com', content='Купіть щось', is_approved=False),
        Comment(post_id=post2.id, author_name='Читач3', author_email='r3@mail.com', content='Корисно', is_approved=True),
    ])
    db.session.commit()
    print(f"✅ Створено 4 коментарі\n")


def read_data():
    """READ."""
    print("=" * 60)
    print("2. READ — вибірки даних")
    print("=" * 60)

    print("\n2.1. filter() — опубліковані статті:")
    published = Post.query.filter_by(status='published').all()
    for p in published:
        print(f"   - {p.title} (автор: {p.author.name})")

    print("\n2.2. filter() з умовою — статті НЕ автора 'Іван Петренко':")
    not_ivan = Post.query.join(Author).filter(Author.name != 'Іван Петренко').all()
    for p in not_ivan:
        print(f"   - {p.title} (автор: {p.author.name})")

    print("\n2.3. or_() — аналог Q-об'єктів OR:")
    from sqlalchemy import or_
    q_or = Post.query.filter(or_(Post.title.ilike('%Python%'), Post.title.ilike('%Flask%'))).all()
    for p in q_or:
        print(f"   - {p.title}")

    print("\n2.4. not_() — аналог Q-об'єктів NOT:")
    from sqlalchemy import not_
    q_not = Post.query.filter(not_(Post.title.ilike('%Django%'))).all()
    for p in q_not:
        print(f"   - {p.title}")

    print("\n2.5. Ланцюжок умов:")
    chain = Post.query.filter_by(status='published').join(Author).filter(Author.name == 'Іван Петренко').all()
    for p in chain:
        print(f"   - {p.title}")
    print()


def aggregation():
    """Агрегація."""
    print("=" * 60)
    print("3. АГРЕГАЦІЯ")
    print("=" * 60)

    from sqlalchemy import func

    print("\n3.1. Загальна статистика:")
    total = db.session.query(func.count(Post.id)).scalar()
    published = db.session.query(func.count(Post.id)).filter(Post.status == 'published').scalar()
    print(f"   Всього статей: {total}")
    print(f"   Опубліковано: {published}")

    print("\n3.2. Кількість коментарів до кожної статті:")
    results = db.session.query(Post.title, func.count(Comment.id)).outerjoin(Comment).group_by(Post.id).all()
    for title, count in results:
        print(f"   - {title}: {count} коментарів")

    print("\n3.3. Статей на автора:")
    author_stats = db.session.query(Author.name, func.count(Post.id)).join(Post).group_by(Author.id).all()
    for name, count in author_stats:
        print(f"   - {name}: {count} статей")
    print()


def transaction_demo():
    """ДЕМОНСТРАЦІЯ ТРАНЗАКЦІЙ."""
    print("=" * 60)
    print("4. ТРАНЗАКЦІЙНА АТОМАРНІСТЬ")
    print("=" * 60)

    # 4.1. Успішна транзакція (commit)
    print("\n4.1. Успішна транзакція (commit):")
    try:
        new_post = Post(title='Транзакційна стаття', slug='tx-post', author_id=1, content='Тест', status='draft')
        new_comment = Comment(post_id=1, author_name='Тест', author_email='t@t.com', content='Тест', is_approved=True)
        db.session.add(new_post)
        db.session.add(new_comment)
        db.session.commit()
        print(f"   ✅ Транзакція успішна: створено '{new_post.title}' та коментар")
    except Exception as e:
        db.session.rollback()
        print(f"   ❌ Помилка: {e}")

    # 4.2. Транзакція з відкатом (rollback)
    print("\n4.2. Транзакція з відкатом (rollback) при помилці:")
    try:
        bad_post = Post(title='Погана стаття', slug='tx-post', author_id=1, content='Тест', status='draft')  # дубль slug!
        db.session.add(bad_post)
        db.session.commit()
        print(f"   ❌ Не повинно було спрацювати!")
    except Exception as e:
        db.session.rollback()
        print(f"   ✅ Транзакцію відкачено: {type(e).__name__}")
        print(f"   Дані залишились незмінними завдяки rollback()")
    print()


def optimization():
    """Оптимізація."""
    print("=" * 60)
    print("5. ОПТИМІЗАЦІЯ ЗАПИТІВ")
    print("=" * 60)

    print("\n5.1. Завантаження зв'язаних об'єктів (joinedload):")
    from sqlalchemy.orm import joinedload
    posts = Post.query.options(joinedload(Post.author)).all()
    for p in posts:
        print(f"   - {p.title} (автор: {p.author.name})")

    print("\n5.2. Зворотні зв'язки (backref):")
    author = db.session.get(Author, 1)
    print(f"   Автор: {author.name}")
    print(f"   Його статті: {[p.title for p in author.posts]}")
    print(f"   Його профіль: {author.profile.website if author.profile else 'немає'}")
    print()


def update_and_delete():
    """UPDATE та DELETE."""
    print("=" * 60)
    print("6. UPDATE та DELETE")
    print("=" * 60)

    print("\n6.1. UPDATE через save():")
    post = Post.query.filter_by(slug='intro-python').first()
    post.title = 'Вступ до Python 3.15'
    db.session.commit()
    print(f"   ✅ Оновлено: '{post.title}'")

    print("\n6.2. Масове UPDATE:")
    updated = Post.query.filter_by(status='draft').update({'status': 'published'})
    db.session.commit()
    print(f"   ✅ Переведено в 'published': {updated} статей")

    print("\n6.3. DELETE з CASCADE:")
    post_to_delete = Post.query.filter_by(slug='draft-post').first()
    if post_to_delete:
        db.session.delete(post_to_delete)
        db.session.commit()
        print(f"   ✅ Видалено статтю (коментарі видалені через CASCADE)")

    print("\n6.4. Масове DELETE:")
    deleted = Comment.query.filter_by(is_approved=False).delete()
    db.session.commit()
    print(f"   ✅ Видалено не схвалених коментарів: {deleted}")
    print()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        clear_data()
        create_data()
        read_data()
        aggregation()
        transaction_demo()
        optimization()
        update_and_delete()
        print("Демо ORM-запитів Flask завершено!")