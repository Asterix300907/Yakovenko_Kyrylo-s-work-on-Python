import pytest
from unittest.mock import patch, MagicMock
import os
from datetime import datetime
from app import app
from models import db, Author


@pytest.fixture
def app_context():
    """Фікстура для створення тестового контексту додатка."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def test_mock_external_file_check(app_context):
    """
    Мок ЗОВНІШНЬОЇ залежності: імітуємо перевірку існування файлу через os.path.exists.
    Це необхідно, щоб тести не залежали від реальної файлової системи,
    що робить їх швидкими та надійними.
    """
    with patch('os.path.exists', return_value=True) as mock_exists:
        result = os.path.exists('/fake/path/config.txt')
        
        assert result is True
        mock_exists.assert_called_once_with('/fake/path/config.txt')


def test_mock_internal_datetime(app_context):
    """
    Мок ВНУТРІШНЬОЇ залежності: імітуємо datetime.utcnow() з модуля models.
    Це необхідно для детермінованого тестування з фіксованим часом.
    """
    fixed_time = datetime(2026, 11, 8, 12, 0, 0)
    
    # Патчимо саме models.datetime, а не datetime.datetime
    with patch('models.datetime') as mock_datetime:
        mock_datetime.utcnow.return_value = fixed_time
        
        # Просто перевіряємо, що мок працює
        result = mock_datetime.utcnow()
        assert result == fixed_time
        mock_datetime.utcnow.assert_called()