from flask import Flask, g
from flask_cors import CORS
from WebDownloader.core.config import set_config
from WebDownloader.core.extensions.celeryClient import set_celery
from WebDownloader.core.extensions.redisClient import set_redis

config = set_config()
celery = set_celery(config)
redis = set_redis(config)

# taskView = TaskView()
flask = Flask(__name__, static_folder=str(config.opt['DATA_LOCATION'].absolute()))
flask.config.from_object(config)
CORS(flask)
g.redis = redis
g.celery = celery

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    r.init_app(app)

    with app.app_context():
        # Include our Routes
        from . import routes

        # Register Blueprints
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(admin.admin_bp)

        return app


# Register views
from .routes import *
