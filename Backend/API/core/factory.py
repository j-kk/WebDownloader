from WebDownloader.core.factory import Module
from flask import Flask


class FModule(Module):
    flask: Flask
    def set_flask(self, **kwargs):
        """Flask instantiation."""
        # Flask instance creation
        self.flask = Flask(__name__, static_folder=str(self.config.opt['DATA_LOCATION'].absolute()), **kwargs)

        # Flask configuration
        self.flask.config.from_object(self.config)

        # Swagger documentation
        self.flask.config.SWAGGER_UI_DOC_EXPANSION = 'list'
        self.flask.config.SWAGGER_UI_JSONEDITOR = True

        return self.flask


    def register_blueprint(self, blueprint, **kwargs):
        """Register a specified backend blueprint."""
        self.flask.register_blueprint(blueprint, **kwargs)

