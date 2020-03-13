"""Initialization module of Resources."""
from flask import Blueprint
from flask_restful import Api
from API.resources.handlers import TextHandler, ImageHandler, StateChecker, GetResult


blueprint = Blueprint('api', __name__, url_prefix='/api')

# API instantiation
api = Api(blueprint)

# Namespaces registration
api.add_resource(TextHandler, '/downloadText')
api.add_resource(ImageHandler, '/downloadImages')
api.add_resource(StateChecker, '/checkState')
api.add_resource(GetResult, '/getResult')

