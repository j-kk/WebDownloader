"""Factory module."""
from flask import Flask
from celery import Celery

from app.core.config import config

# System based imports
import os

class Module():
    """Build the instances needed for the app."""
    config = {}

    def __init__(self, environment='default'):
        """Initialize Factory with the proper environment."""
        # Get the running environment
        self._environment = os.getenv("APP_ENVIRONMENT")
        if not self._environment:
            self._environment = environment

        self._config_template = config[self._environment]

        for key in dir(self._config_template):
            if key.isupper():
                self.config[key] = getattr(self._config_template, key)


    @property
    def environment(self):
        """Getter for environment attribute."""
        return self._environment

    @environment.setter
    def environment(self, environment):
        # Update environment protected variable
        self._environment = environment

        # Update Flask configuration (if enabled)
        if self.flask:
            self.flask.config.from_object(config[self._environment])

        # Update Celery Configuration
        self.celery.conf.update(self.config)

    def set_flask(self, **kwargs):
        """Flask instantiation."""
        # Flask instance creation
        self.flask = Flask(__name__, **kwargs)

        # Flask configuration
        self.flask.config.from_object(config[self._environment])

        # Swagger documentation
        self.flask.config.SWAGGER_UI_DOC_EXPANSION = 'list'
        self.flask.config.SWAGGER_UI_JSONEDITOR = True

        return self.flask

    def set_celery(self, **kwargs):
        """Celery instantiation."""
        # Celery instance creation
        self.celery = Celery(__name__, broker=self.config['CELERY_BROKER_URL'], backend=self.config['CELERY_RESULT_BACKEND'])

        # Celery Configuration
        self.celery.conf.update(self.config)

        return self.celery

    def register_blueprint(self, blueprint):
        """Register a specified api blueprint."""
        self.flask.register_blueprint(blueprint)

