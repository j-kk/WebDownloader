"""Application Configuration."""
import os
from pathlib import Path


class ConfigTemplate(object):
    """Parent configuration class."""

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')

    TITLE = "Text and images downloader from webpages"
    VERSION = "0.1.0"
    DESCRIPTION = "An REST WebDownloader to download images and text from webpages. Made with flask & celeryClient."

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    BROKER_URL: str

    DATA_LOCATION: str

    def __init__(self):
        self.CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL') if None else 'redis://localhost:6379/0'
        self.CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND') if None else 'redis://localhost:6379/0'
        self.BROKER_URL = self.CELERY_BROKER_URL

        if os.getenv('DATA_LOCATION') is None:
            raise Exception('DATA_LOCATION not set!')

        self.DATA_LOCATION = Path(os.getenv('DATA_LOCATION'))


class DevelopmentConfig(ConfigTemplate):
    """Configurations for Development."""

    DEBUG = True


class TestingConfig(ConfigTemplate):
    """Configurations for Testing."""

    TESTING = True
    DEBUG = True

    CELERY_ALWAYS_EAGER = True


class ProductionConfig(ConfigTemplate):
    """Configurations for Production."""

    DEBUG = False
    TESTING = False

    def __init__(self):
        super().__init__()
        self.CELERY_BROKER_URL = 'redis://redis:6379/0'
        self.CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
        self.BROKER_URL = self.CELERY_BROKER_URL


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


class Config(object):
    """App configuration specification,
        gets information from env variables
        or from template

    """

    def __init__(self, environment):
        """Initialize Config with the proper environment."""
        # Get the running environment
        self.environment = environment

        # Get variables from template
        self._config_template = config[self.environment]()
        self.opt = {}
        for key in dir(self._config_template):
            if key.isupper():
                self.opt[key] = getattr(self._config_template, key)

        if not self.opt['DATA_LOCATION'].is_dir():
            self.opt['DATA_LOCATION'].mkdir()

    def __getitem__(self, item):
        return self.opt[item]
