from WebDownloader.api.task import TaskView
from WebDownloader.core.factory import Module

#create module
module = Module()
# Enable flask instance
module.set_flask()
# Enable celeryClient connection
module.set_celery()
#Create task view
taskView = TaskView()


# Register the api blueprint
module.register_blueprint(taskView.createBlueprint(module.flask, module.celeryClient))

# Get flask instance
flask = module.flask

if __name__ == '__main__':
    flask.run()