from redis.client import Redis
from flask import Flask, send_from_directory
from flask_restful import Resource, reqparse
from WebDownloader.jobs.celery import CeleryClient

class StateChecker(Resource):
    """
    Handles api state checking
    """

    def __init__(self, celeryClient: CeleryClient, redisClient: Redis, **kwargs):
        self.celeryClient = celeryClient
        self.redisClient = redisClient
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type=str, required=True,
                                   help='Task ID', action='append')
        super().__init__()

    def post(self):
        """Checks api's states
        :return: tasks states
        """
        args = self.reqparse.parse_args()
        ret = []
        for task_id in args['id']:
            if task_id == None:
                continue
            if self.redisClient.exists(task_id) == 0:
                continue
            status = self.celeryClient.check_state(task_id)
            metadata = self.redisClient.hgetall(task_id)
            ret.append({
                'task_id': task_id,
                'state': status,
                'time': metadata['time'],
                'type': metadata['type'],
            })
            if status == 'SUCCESS':
                ret[-1]['filename'] = self.celeryClient.get_result_name(task_id)
        return ret, 201 if len(ret) > 0 else 404


class GetResult(Resource):
    """
    Handles result queries
    """
    flaskInstance: Flask

    def __init__(self, celeryClient: CeleryClient, flaskInstance: Flask, **kwargs):
        self.celeryClient = celeryClient
        self.flaskInstance = flaskInstance
        super().__init__()

    def get(self, filename):
        """Returns api result
        :return: api result
        """
        return send_from_directory(self.flaskInstance.static_folder, filename)  # TODO replace becouse it's slow

