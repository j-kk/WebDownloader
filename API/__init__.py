"""Initialization module of the package."""
# API Factory imports
from API.factory import Factory

# API configuration imports
from API.config import Config

# Instantiation of the factory
factory = Factory()

# Enable flask instance
factory.set_flask()

# Enable of the desired plugins
factory.set_celery()

# API Resources imports
from API.resources import blueprint

# Register the blueprint
factory.register(blueprint)
