import flask
import validators
from flask import send_from_directory
from flask_restful import Resource, reqparse

from WebDownloader.core.helpers.webres import get_url
from WebDownloader.jobs.celery import CeleryServer
from WebDownloader.jobs.tasks import ExtendedTask


class TaskHandler(Resource):

    task: ExtendedTask

    def __init__(self, task: ExtendedTask):
        self.task = task
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type=str, required=True,
                                   help='URL to website', action='append')
        super().__init__()

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
            task_id = self.task.delay(url).id
            ret.append({
                'url': url,
                'task_id': task_id
            })
        return ret, 201 if len(ret) > 0 else 406

class TextHandler(TaskHandler):
    """
    Handles textTask requests
    """

    def __init__(self, celery: CeleryServer, **kwargs):
        super().__init__(task=celery.textTask)


class ImageHandler(TaskHandler):
    def __init__(self, celery: CeleryServer, **kwargs):
        super().__init__(task=celery.imageTask)



class IDHandler(Resource):

    def __init__(self, celery: CeleryServer):
        self.celery = celery
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type=str, required=True,
                                   help='Task ID', action='append')
        super().__init__()



class StateChecker(IDHandler):
    """
    Handles task state checking
    """

    def __init__(self, celery: CeleryServer, **kwargs):
        super().__init__(celery)

    def post(self):
        """Checks task's states
        :return: tasks states
        """
        args = self.reqparse.parse_args()
        ret = []
        for task_id in args['id']:
            status = self.celery.check_state(task_id)
            ret.append({
                'task_id': task_id,
                'state': status
            })
        return ret, 201 if len(ret) > 0 else 406


class GetResult(IDHandler):
    """
    Handles result queries
    """
    flaskInstance: flask

    def __init__(self, celery: CeleryServer, flaskInstance: flask):
        super().__init__(celery)
        self.flaskInstance = flaskInstance #TODO change

    def get(self):
        """Returns task result
        :return: task result
        """
        args = self.reqparse.parse_args()
        task_id = args['id'][0]
        if self.celery.check_state(task_id) == 'SUCCESS':
            file_name = self.celery.find_result(task_id)
            return send_from_directory(self.flaskInstance.static_folder, file_name)  # TODO replace beacouse it's slow

        return {}, 404
