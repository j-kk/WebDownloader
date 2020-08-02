import datetime

import redis
import validators
from flask_restful import Resource, reqparse

from WebDownloader.core.helpers import get_url
from WebDownloader.jobs.celery import CeleryClient
from WebDownloader.jobs.tasks import ExtendedTask


class TaskHandler(Resource):
    redisClient: redis.client.Redis
    task: ExtendedTask

    def __init__(self, task: ExtendedTask, redisClient: redis.client.Redis):
        self.task = task
        self.redisClient = redisClient
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
            task_data = {
                'time': str(datetime.datetime.now()),
                'type': self.task.__name__,
            }
            self.redisClient.hset(task_id, None, None, task_data)
            ret.append({
                'url': url,
                'task_id': task_id
            })
        return ret, 201 if len(ret) > 0 else 406


class TextHandler(TaskHandler):
    """
    Handles textTask requests
    """

    def __init__(self, celeryClient: CeleryClient, redisClient: redis.client.Redis, **kwargs):
        super().__init__(task=celeryClient.textTask, redisClient=redisClient)


class ImageHandler(TaskHandler):
    def __init__(self, celeryClient: CeleryClient, redisClient: redis.client.Redis, **kwargs):
        super().__init__(task=celeryClient.imageTask, redisClient=redisClient)


class WebCrawlHandler(TaskHandler):
    def __init__(self, celeryClient: CeleryClient, redisClient: redis.client.Redis, **kwargs):
        super().__init__(task=celeryClient.webCrawlTask, redisClient=redisClient)