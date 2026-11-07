from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    """Автор статей."""
    name = models.CharField(max_length=100, verbose_name="Ім'я автора")
    email = models.EmailField(unique=True, verbose_name="Електронна пошта")
    bio = models.TextField(blank=True, verbose_name="Біографія")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    class Meta:
        ordering = ['name']
        verbose_name = "Автор"
        verbose_name_plural = "Автори"

    def __str__(self):
        return self.name


class Profile(models.Model):
    """Профіль автора (OneToOne зв'язок)."""
    author = models.OneToOneField(
        Author, 
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    website = models.URLField(blank=True, verbose_name="Веб-сайт")
    social_media = models.CharField(max_length=200, blank=True, verbose_name="Соціальні мережі")

    class Meta:
        verbose_name = "Профіль"
        verbose_name_plural = "Профілі"

    def __str__(self):
        return f"Профіль {self.author.name}"


class Tag(models.Model):
    """Тег для статей (ManyToMany зв'язок)."""
    name = models.CharField(max_length=50, unique=True, verbose_name="Назва тегу")
    slug = models.SlugField(unique=True, verbose_name="URL-ідентифікатор")

    class Meta:
        ordering = ['name']
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Post(models.Model):
    """Стаття блогу."""
    STATUS_CHOICES = [
        ('draft', 'Чернетка'),
        ('published', 'Опубліковано'),
    ]

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, verbose_name="URL-ідентифікатор")
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name='posts'
    )
    content = models.TextField(verbose_name="Зміст")
    tags = models.ManyToManyField(
        Tag, 
        blank=True,
        related_name='posts',
        verbose_name="Теги"
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='draft',
        verbose_name="Статус"
    )
    views_count = models.IntegerField(default=0, verbose_name="Кількість переглядів")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Стаття"
        verbose_name_plural = "Статті"

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Коментар до статті."""
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE,
        verbose_name="Стаття",
        related_name='comments'
    )
    author_name = models.CharField(max_length=100, verbose_name="Ім'я коментатора")
    author_email = models.EmailField(verbose_name="Email коментатора")
    content = models.TextField(verbose_name="Текст коментаря")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    is_approved = models.BooleanField(default=False, verbose_name="Схвалено")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"

    def __str__(self):
        return f"Коментар від {self.author_name} до {self.post.title}"