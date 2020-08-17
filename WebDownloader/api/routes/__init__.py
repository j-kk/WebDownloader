# from flask import Flask, Blueprint
# from .views import StateChecker, GetResult
# from .new_tasks import TextHandler, ImageHandler, WebCrawlHandler
# from .new_tasks import *
from .views import *

# class TaskView(object):
#
#     def createBlueprint(self, flaskInstance: Flask, celery: CeleryClient, redisClient: Redis):
#         kwargs = {
#             'celeryClient': celery,
#             'flaskInstance': flaskInstance,
#             'redisClient': redisClient
#         }
#         self.api.add_resource(TextHandler, '/getText', resource_class_kwargs=kwargs)
#         self.api.add_resource(ImageHandler, '/getImages', resource_class_kwargs=kwargs)
#         self.api.add_resource(WebCrawlHandler, '/crawlWebsite', resource_class_kwargs=kwargs)
#         self.api.add_resource(StateChecker, '/checkState', resource_class_kwargs=kwargs)
#         self.api.add_resource(GetResult, '/downloadResult/<filename>', resource_class_kwargs=kwargs)
#         return self.blueprint
#
#
#     def __init__(self):
#         self.blueprint = Blueprint(name='taskHandler', import_name='tHandler')
#         self.api = Api(self.blueprint)

