"""Factory module."""
from flask import Flask

from WebDownloader.core.config import Config
# System based imports
import os

from WebDownloader.jobs.celery import CeleryServer


class Module():
    """Build the instances needed for the WebDownloader."""
    config: Config

    def __init__(self, environment='default'):
        """Initialize Factory with the proper environment."""
        # Get the running environment
        self._environment = os.getenv("APP_ENVIRONMENT")
        if not self._environment:
            self._environment = environment

        self.config = Config(self._environment)


    @property
    def environment(self):
        """Getter for environment attribute."""
        return self._environment

    @environment.setter
    def environment(self, value):
        self._environment = value

    def __getitem__(self, item):
        return self.config[item]

    def set_flask(self, **kwargs) -> Flask:
        """Flask instantiation."""
        # Flask instance creation
        self.flask = Flask(__name__, static_folder=self.config.opt['DATA_LOCATION'], **kwargs)

        # Flask configuration
        self.flask.config.from_object(self.config)

        # Swagger documentation
        self.flask.config.SWAGGER_UI_DOC_EXPANSION = 'list'
        self.flask.config.SWAGGER_UI_JSONEDITOR = True

        return self.flask

    def set_celery(self, **kwargs) -> CeleryServer:
        """Celery instantiation."""
        # Celery instance creation
        self.celery = CeleryServer(self.config, **kwargs)

        return self.celery

    def register_blueprint(self, blueprint, **kwargs):
        """Register a specified api blueprint."""
        self.flask.register_blueprint(blueprint, **kwargs)

