from flask import Flask
from flask_cors import CORS
from flask_redis import FlaskRedis
from core.config import config
from core.extensions.celery.celeryClient import set_celery
from core.extensions.redisClient import set_redis

celery = set_celery()
redis = FlaskRedis.from_custom_provider(set_redis(), decode_responses=True)


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False, static_folder=str(config.opt['DATA_LOCATION'].absolute()))
    app.config.from_object(config)
    CORS(app)

    # Initialize Plugins
    redis.init_app(app)

    with app.app_context():
        # Include our Routes
        from . import routes

        # Register Blueprints
        app.register_blueprint(routes.task_view)
        app.register_blueprint(routes.new_tasks)

        return app