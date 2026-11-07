import pytest
from unittest.mock import patch, MagicMock
import smtplib
from django.utils import timezone
from blog.models import Author, Post


@pytest.mark.django_db
def test_mock_external_email():
    """
    Мок ЗОВНІШНЬОЇ залежності: імітуємо надсилання email через SMTP.
    Це необхідно, щоб тести не залежали від реального поштового сервера,
    що робить їх швидкими та надійними.
    """
    with patch('smtplib.SMTP') as mock_smtp_class:
        mock_server = MagicMock()
        mock_smtp_class.return_value = mock_server
        
        
        server = smtplib.SMTP('smtp.example.com', 587)
        server.sendmail('admin@blog.com', 'user@test.com', 'Welcome!')
        server.quit()
        
        mock_smtp_class.assert_called_once_with('smtp.example.com', 587)
        mock_server.sendmail.assert_called_once_with(
            'admin@blog.com', 'user@test.com', 'Welcome!'
        )


@pytest.mark.django_db
def test_mock_internal_datetime():
    """
    Мок ВНУТРІШНЬОЇ залежності: імітуємо поточний час.
    Це необхідно для детермінованого тестування (фіксований час).
    """
    fixed_time = timezone.datetime(2026, 11, 8, 12, 0, 0, tzinfo=timezone.UTC)
    
    with patch('django.utils.timezone.now', return_value=fixed_time):
        author = Author.objects.create(name='Тест Часу', email='time@test.com')
        post = Post.objects.create(
            title='Тестова стаття',
            slug='test-post',
            author=author,
            content='Тестовий контент',
            status='published'
        )
        
        assert post.created_at is not None
        assert timezone.now() == fixed_time