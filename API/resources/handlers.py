from flask_restful import Resource, reqparse
from celery.result import AsyncResult
from API import factory
from API.resources.tasks import textTask

parser = reqparse.RequestParser()

class TextHandler(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type = str, required = True,
                                   help = 'URL to website', location = 'args')
        super(TextHandler, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        url = args['url']
        task = textTask.delay(url)
        return {"task_id": task.task_id }, 200

class ImageHandler(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type = str, required = True,
                                   help = 'URL to website', location = 'args')
        super(ImageHandler, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        url = args['url']

        return {"message": f'Hello {url}!'}

class StateChecker(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, required = True,
                                   help = 'Task ID', location = 'args')
        super(StateChecker, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        task_id = args['id']
        status = factory.celery.AsyncResult(task_id).status
        if status == 'PENDING':
            status = 'NOT FOUND'
        return {task_id: status}

class GetResult(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, required = True,
                                   help = 'Task ID', location = 'args')
        super(GetResult, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        pass

        return {"message": f'Hello !'}
