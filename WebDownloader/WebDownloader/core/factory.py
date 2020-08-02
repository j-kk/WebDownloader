"""Factory module."""
# System based imports
import os
import redis
from flask import Flask
from flask_cors import CORS
from celery import Celery

from WebDownloader.core.config import Config
from WebDownloader.jobs.celery import CeleryClient

class Module():
    """Build the instances needed for the WebDownloader."""
    config: Config
    redis: redis.client.Redis

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

    def set_flask(self, **kwargs):
        """Flask instantiation."""
        # Flask instance creation
        self.flask = Flask(__name__, static_folder=str(self.config.opt['DATA_LOCATION'].absolute()), **kwargs)

        # Flask configuration
        self.flask.config.from_object(self.config)

        # CORS
        CORS(self.flask)

        return self.flask


    def register_blueprint(self, blueprint, **kwargs):
        """Register a specified backend blueprint."""
        self.flask.register_blueprint(blueprint, **kwargs)

    def set_celery(self, **kwargs) -> Celery:
        """Celery instantiation."""
        # Celery instance creation
        self.celeryClient = CeleryClient(self.config, **kwargs)

        return self.celeryClient.celery

    def set_redis(self, **kwargs):
        self.redis = redis.Redis(self.config['REDIS_URL'], self.config['REDIS_PORT'], decode_responses=True)


