"""Application Configuration."""
import os
from pathlib import Path


class Config(object):
    """Parent configuration class."""

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')

    TITLE = "Text and images downloader from webpages"
    VERSION = "0.1.0"
    DESCRIPTION = "An REST WebDownloader to download images and text from webpages. Made with flask & celery."

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    BROKER_URL = CELERY_BROKER_URL

    DATA_LOCATION = Path(os.getenv('DATA_LOCATION') if None else Path("./db").absolute())


class DevelopmentConfig(Config):
    """Configurations for Development."""

    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing."""

    TESTING = True
    DEBUG = True

    CELERY_ALWAYS_EAGER = True


class StagingConfig(Config):
    """Configurations for Staging."""

    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""

    DEBUG = False
    TESTING = False

    CELERY_BROKER_URL = 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
    BROKER_URL = CELERY_BROKER_URL


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
