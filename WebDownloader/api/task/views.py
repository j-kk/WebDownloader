import validators
from flask import Blueprint
from flask import send_from_directory
from flask_restful import Api, Resource, reqparse

from WebDownloader.jobs import module
from WebDownloader.core.helpers.webres import get_url
from WebDownloader.jobs.task_management import check_state, find_result
from WebDownloader.jobs.tasks import textTask, imageTask

taskHandlerBp = Blueprint(name='taskHandler', import_name='tHandler')
api = Api(taskHandlerBp)


@api.resource('/getText')
class TextHandler(Resource):
    """
    Handles textTask requests
    """

    def __init__(self, *args, **kwargs):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type=str, required=True,
                                   help='URL to website', action='append')
        super(TextHandler, self).__init__()

    def post(self):
        """On post schedules textTask
        :return: id's of created tasks
        """
        args = self.reqparse.parse_args()
        ret = []
        for i, url in enumerate(args['url']):
            url = get_url(url)
            if not validators.url(url):
                continue
            task_id = textTask.delay(url).id
            ret.append({
                'url': url,
                'task_id': task_id
            })
        return ret, 201 if len(ret) > 0 else 406


@api.resource('/getImages')
class ImageHandler(Resource): #TODO unify with TextHandler
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type=str, required=True,
                                   help='URL to website', action='append')
        super(ImageHandler, self).__init__()

    def post(self):
        """On post schedules imageTasks
        :return: id's of created tasks
        """
        args = self.reqparse.parse_args()
        ret = []
        for i, url in enumerate(args['url']):
            url = get_url(url)
            if not validators.url(url):
                continue
            task_id = imageTask.delay(url).id
            ret.append({
                'url': url,
                'task_id': task_id
            })

        return ret, 201 if len(ret) > 0 else 406


@api.resource('/checkState')
class StateChecker(Resource):
    """
    Handles task state checking
    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type=str, required=True,
                                   help='Task ID', action='append')
        super(StateChecker, self).__init__()

    def post(self):
        """Checks task's states
        :return: tasks states
        """
        args = self.reqparse.parse_args()
        ret = []
        for task_id in args['id']:
            status = check_state(task_id)
            ret.append({
                'task_id': task_id,
                'state': status
            })
        return ret, 201 if len(ret) > 0 else 406


@api.resource('/downloadResult')
class GetResult(Resource):
    """
    Handles result queries
    """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type=str, required=True,
                                   help='Task ID', action='append')
        super(GetResult, self).__init__()

    def get(self):
        """Returns task result
        :return: task result
        """
        args = self.reqparse.parse_args()
        task_id = args['id'][0]
        if check_state(task_id) == 'SUCCESS':
            file_name = find_result(task_id)
            return send_from_directory(module.flask.static_folder, file_name)  # TODO replace beacouse it's slow

        return {}, 404
