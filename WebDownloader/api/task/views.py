from flask import Blueprint
from flask import send_from_directory
from flask_restful import Api, Resource, reqparse

from WebDownloader.jobs import module
from WebDownloader.core.helpers.webres import get_url
from WebDownloader.jobs.task_management import check_state, find_result
from WebDownloader.jobs.tasks import textTask, imageTask

taskHandlerBp = Blueprint(name='taskHandler', import_name='tHandler')
api = Api(taskHandlerBp)

# website_url = api.model('URL', {
#     'url': fields.Url(required=True, description='URL to website', absolute=True)
# })
#
# task_id = api.model('ID', {
#     'task_id': fields.String(required=True, description='Task ID')
# })
#
# task_state = api.model('STATE', {
#     'task_id': fields.String(required=True, description='Task ID'),
#     'state': fields.String(required=True, description='Task state')
# })

@api.resource('/getText')
class TextHandler(Resource):
    def __init__(self, *args, **kwargs):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type = str, required = True,
                                   help = 'URL to website', action='append')
        super(TextHandler, self).__init__()

    # @api.expect([website_url])
    # @api.marshal_with(website_url)
    def post(self):
        args = self.reqparse.parse_args()
        ret = []
        for i, url in enumerate(args['url']):
            url = get_url(url)
            task_id = textTask.delay(url).id
            ret.append({'task_id': task_id})
        return ret

@api.resource('/getImages')
class ImageHandler(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type = str, required = True,
                                   help = 'URL to website', action='append')
        super(ImageHandler, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        ret = []
        for i, url in enumerate(args['url']):
            url = get_url(url)
            task_id = imageTask.delay(url).id
            ret.append({'task_id':task_id})
        return ret

@api.resource('/checkState')
class StateChecker(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, required = True,
                                   help = 'Task ID', action='append')
        super(StateChecker, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        ret = []
        for task_id in args['id']:
            status = check_state(task_id)
            ret.append({
                'task_id': task_id,
                'state': status
            })
        return ret

@api.resource('/downloadResult')
class GetResult(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, required = True,
                                   help = 'Task ID', action='append')
        super(GetResult, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        task_id = args['id']
        if check_state(task_id) == 'SUCCESS':
            file = find_result(task_id)
            if file is not None:
                return send_from_directory(module.config['DATA_LOCATION'], file)

        return {}, 404
