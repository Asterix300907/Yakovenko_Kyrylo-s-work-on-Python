"""Демонстрація ORM-запитів Django."""

import os
import django

# Налаштування Django перед імпортом моделей
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from blog.models import Author, Profile, Tag, Post, Comment
from django.db.models import Q, Count, Avg, Sum
from django.db.models.functions import Length 


def clear_data():
    """Очистити базу перед демо."""
    Comment.objects.all().delete()
    Post.objects.all().delete()
    Tag.objects.all().delete()
    Profile.objects.all().delete()
    Author.objects.all().delete()
    print("✅ База очищена\n")


def create_data():
    """Створити тестові дані (CREATE)."""
    print("=" * 60)
    print("1. CREATE — створення даних")
    print("=" * 60)

    # Створення авторів
    author1 = Author.objects.create(name='Іван Петренко', email='ivan@example.com', bio='Досвідчений розробник')
    author2 = Author.objects.create(name='Марія Сидоренко', email='maria@example.com', bio='Початківець')
    author3 = Author.objects.create(name='Олексій Коваль', email='alex@example.com', bio='Технічний письменник')
    print(f"✅ Створено 3 авторів: {author1}, {author2}, {author3}")

    # Створення профілів (OneToOne)
    Profile.objects.create(author=author1, website='https://ivan.blog')
    Profile.objects.create(author=author2, website='https://maria.blog')
    print("✅ Створено 2 профілі")

    # Створення тегів
    python_tag = Tag.objects.create(name='Python', slug='python')
    django_tag = Tag.objects.create(name='Django', slug='django')
    flask_tag = Tag.objects.create(name='Flask', slug='flask')
    print(f"✅ Створено 3 теги: {python_tag}, {django_tag}, {flask_tag}")

    # Створення статей
    post1 = Post.objects.create(title='Вступ до Python', slug='intro-python', author=author1, content='Python — це...', status='published')
    post2 = Post.objects.create(title='Django для початківців', slug='django-beginners', author=author1, content='Django — це...', status='published')
    post3 = Post.objects.create(title='Flask vs Django', slug='flask-vs-django', author=author3, content='Порівняння...', status='published')
    post4 = Post.objects.create(title='Чернетка статті', slug='draft-post', author=author2, content='Ще не готово', status='draft')
    print(f"✅ Створено 4 статті")

    # Додавання тегів до статей (ManyToMany)
    post1.tags.add(python_tag, django_tag)
    post2.tags.add(django_tag, python_tag)
    post3.tags.add(python_tag, flask_tag)
    print(f"✅ Теги додано до статей")

    # Створення коментарів
    Comment.objects.create(post=post1, author_name='Читач1', author_email='r1@mail.com', content='Чудова стаття!', is_approved=True)
    Comment.objects.create(post=post1, author_name='Читач2', author_email='r2@mail.com', content='Дякую!', is_approved=True)
    Comment.objects.create(post=post1, author_name='Спам', author_email='spam@mail.com', content='Купіть щось', is_approved=False)
    Comment.objects.create(post=post2, author_name='Читач3', author_email='r3@mail.com', content='Корисно', is_approved=True)
    print(f"✅ Створено 4 коментарі\n")


def read_data():
    """READ — вибірки (filter, exclude, Q-об'єкти)."""
    print("=" * 60)
    print("2. READ — вибірки даних")
    print("=" * 60)

    # 2.1. Проста фільтрація (filter)
    print("\n2.1. filter() — опубліковані статті:")
    published = Post.objects.filter(status='published')
    for p in published:
        print(f"   - {p.title} (автор: {p.author.name})")

    # 2.2. Виключення (exclude)
    print("\n2.2. exclude() — статті НЕ автора 'Іван Петренко':")
    not_ivan = Post.objects.exclude(author__name='Іван Петренко')
    for p in not_ivan:
        print(f"   - {p.title} (автор: {p.author.name})")

    # 2.3. Q-об'єкти (OR)
    print("\n2.3. Q-об'єкти (OR) — статті з 'Python' АБО 'Flask' у заголовку:")
    q_or = Post.objects.filter(Q(title__icontains='Python') | Q(title__icontains='Flask'))
    for p in q_or:
        print(f"   - {p.title}")

    # 2.4. Q-об'єкти (NOT)
    print("\n2.4. Q-об'єкти (NOT) — статті БЕЗ слова 'Django' у заголовку:")
    q_not = Post.objects.filter(~Q(title__icontains='Django'))
    for p in q_not:
        print(f"   - {p.title}")

    # 2.5. Ланцюжок умов
    print("\n2.5. Ланцюжок: опубліковані статті автора 'Іван Петренко':")
    chain = Post.objects.filter(status='published').filter(author__name='Іван Петренко')
    for p in chain:
        print(f"   - {p.title}")
    print()


def aggregation():
    """Агрегація та анотація."""
    print("=" * 60)
    print("3. АГРЕГАЦІЯ ТА АНОТАЦІЯ")
    print("=" * 60)

    # 3.1. Aggregate — загальна статистика
    print("\n3.1. aggregate() — загальна статистика:")
    stats = Post.objects.aggregate(
        total_posts=Count('id'),
        published_posts=Count('id', filter=Q(status='published')),
        avg_title_length=Avg(Length('title'))
    )
    print(f"   Всього статей: {stats['total_posts']}")
    print(f"   Опубліковано: {stats['published_posts']}")
    print(f"   Середня довжина заголовка: {stats['avg_title_length']:.1f} символів")

    # 3.2. Annotate — кількість коментарів для кожної статті
    print("\n3.2. annotate() — кількість коментарів до кожної статті:")
    posts_with_comments = Post.objects.annotate(comment_count=Count('comments'))
    for p in posts_with_comments:
        print(f"   - {p.title}: {p.comment_count} коментарів")

    # 3.3. Annotate — кількість тегів
    print("\n3.3. annotate() — кількість тегів для кожної статті:")
    posts_with_tags = Post.objects.annotate(tag_count=Count('tags'))
    for p in posts_with_tags:
        print(f"   - {p.title}: {p.tag_count} тегів")

    # 3.4. Групування через values + annotate
    print("\n3.4. values() + annotate() — статей на автора:")
    authors_stats = Author.objects.annotate(post_count=Count('posts')).values('name', 'post_count')
    for a in authors_stats:
        print(f"   - {a['name']}: {a['post_count']} статей")
    print()


def optimization():
    """Оптимізація запитів: select_related, prefetch_related."""
    print("=" * 60)
    print("4. ОПТИМІЗАЦІЯ ЗАПИТІВ")
    print("=" * 60)

    # 4.1. Без оптимізації (N+1 проблема)
    print("\n4.1. Без select_related (N+1 проблема):")
    print("   Кількість SQL-запитів: 1 (для статей) + N (для авторів)")
    posts = Post.objects.all()
    for p in posts:
        _ = p.author.name  # Кожен раз окремий запит

    # 4.2. З select_related (JOIN)
    print("\n4.2. З select_related (оптимально для ForeignKey):")
    print("   Кількість SQL-запитів: 1 (з JOIN)")
    posts_opt = Post.objects.select_related('author').all()
    for p in posts_opt:
        _ = p.author.name  # Дані вже завантажені

    # 4.3. prefetch_related для ManyToMany
    print("\n4.3. prefetch_related (оптимально для ManyToMany):")
    print("   Кількість SQL-запитів: 2 (один для статей, один для тегів)")
    posts_prefetch = Post.objects.prefetch_related('tags').all()
    for p in posts_prefetch:
        tags_list = [t.name for t in p.tags.all()]
        print(f"   - {p.title}: теги = {tags_list}")

    # 4.4. Зворотні зв'язки
    print("\n4.4. Зворотні зв'язки (related_name):")
    author = Author.objects.get(name='Іван Петренко')
    print(f"   Автор: {author.name}")
    print(f"   Його статті: {[p.title for p in author.posts.all()]}")
    print(f"   Його профіль: {author.profile.website}")
    print()


def update_data():
    """UPDATE — оновлення даних."""
    print("=" * 60)
    print("5. UPDATE — оновлення даних")
    print("=" * 60)

    # 5.1. Оновлення через save()
    post = Post.objects.get(slug='intro-python')
    post.title = 'Вступ до Python 3.15'
    post.save()
    print(f"✅ Оновлено заголовок: '{post.title}'")

    # 5.2. Оновлення через update() (масове)
    updated = Post.objects.filter(status='draft').update(status='published')
    print(f"✅ Масове оновлення: переведено в 'published' статей: {updated}")

    # 5.3. Оновлення через F-вирази
    from django.db.models import F
    Post.objects.filter(slug='intro-python').update(views_count=F('views_count') + 100)
    post.refresh_from_db()
    print(f"✅ F-вираз: views_count тепер = {post.views_count}")
    print()


def delete_data():
    """DELETE — видалення даних."""
    print("=" * 60)
    print("6. DELETE — видалення даних")
    print("=" * 60)

    # 6.1. Видалення одного об'єкта
    post_to_delete = Post.objects.get(slug='draft-post')
    post_to_delete.delete()
    print(f"✅ Видалено статтю: 'draft-post' (разом з коментарями через CASCADE)")

    # 6.2. Перевірка каскадного видалення
    comments_left = Comment.objects.filter(post__slug='draft-post').count()
    print(f"   Коментарів до видаленої статті залишилось: {comments_left}")

    # 6.3. Масове видалення
    deleted_count, _ = Comment.objects.filter(is_approved=False).delete()
    print(f"✅ Масове видалення: видалено не схвалених коментарів: {deleted_count}")
    print()


if __name__ == '__main__':
    clear_data()
    create_data()
    read_data()
    aggregation()
    optimization()
    update_data()
    delete_data()
    print("🎉 Демо ORM-запитів Django завершено!")