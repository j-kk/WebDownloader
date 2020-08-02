
from .routes import TaskView
from WebDownloader.core.factory import Module

#create module
module = Module()
# Enable flask instance
module.set_flask()
# Enable celeryClient connection
module.set_celery()
# Enable redis
module.set_redis()
#Create task view
taskView = TaskView()


# Register the api blueprint
module.register_blueprint(taskView.createBlueprint(module.flask, module.celeryClient, module.redis))

# Get flask instance
flaskInstance = module.flask





