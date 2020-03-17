import flask
from flask import Blueprint
from flask_restful import Api

from WebDownloader.api.task.views import TextHandler, ImageHandler, StateChecker, GetResult
from WebDownloader.jobs.celery import CeleryServer



class TaskView(object):

    def createBlueprint(self, flaskInstance: flask, celery: CeleryServer):
        kwargs = {
            'celery': celery,
            'flaskInstance': flaskInstance
        }
        self.api.add_resource(TextHandler, '/getText', resource_class_kwargs=kwargs)
        self.api.add_resource(ImageHandler, '/getImages', resource_class_kwargs=kwargs)
        self.api.add_resource(StateChecker, '/checkState', resource_class_kwargs=kwargs)
        self.api.add_resource(GetResult, '/downloadResult', resource_class_kwargs=kwargs)
        return self.blueprint


    def __init__(self):
        self.blueprint = Blueprint(name='taskHandler', import_name='tHandler')
        self.api = Api(self.blueprint)







