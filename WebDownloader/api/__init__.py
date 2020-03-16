"""Initialization module of the package."""
from WebDownloader.core import module

# Enable flask instance
module.set_flask()

from .task import views
# Register the api blueprint
module.register_blueprint(views.taskHandlerBp)

# Get flask instance
flask = module.flask