"""Конфігурація Flask-додатка."""

import os


class Config:
    """Базова конфігурація."""
    SECRET_KEY = 'dev-secret-key-change-in-production'
    DEBUG = False


class DevelopmentConfig(Config):
    """Конфігурація для розробки."""
    DEBUG = True


class ProductionConfig(Config):
    """Конфігурація для production."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')
    DEBUG = False


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}