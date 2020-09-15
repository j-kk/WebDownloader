from flask import Flask
from flask_cors import CORS
from WebDownloader.core.config import config
from WebDownloader.core.extensions.celery.celeryClient import set_celery
from WebDownloader.core.extensions.redisClient import set_redis

celery = set_celery()
redis = set_redis()


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False, static_folder=str(config.opt['DATA_LOCATION'].absolute()))
    app.config.from_object(config.opt)
    CORS(app)


    with app.app_context():
        # Include our Routes
        from . import routes

        # Register Blueprints
        app.register_blueprint(routes.task_view, url_prefix='/api')
        app.register_blueprint(routes.new_tasks, url_prefix='/api')
        app.register_blueprint(routes.health)

        return app