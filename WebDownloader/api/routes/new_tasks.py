import datetime

import validators
from flask import Blueprint, request, jsonify

from core.helpers import get_url
from core.extensions.celery import TextTask, ImageTask, WebCrawlTask
from api.schemas.tasks import WebsiteURLSchema
from api import redis

new_tasks = Blueprint('new_tasks', __name__)

def handleTaskWrapper(task, *args, **kwargs):
    schema = WebsiteURLSchema()
    url_list = schema.load(request.json)
    ret = []
    for url in url_list:
        url = get_url(url)
        if not validators.url(url):
            continue
        task_id = task.delay(url).id
        task_data = {
            'time': str(datetime.datetime.now()),
            'type': task.__name__,
        }
        redis.hset(task_id, None, None, task_data)
        ret.append({
            'url': url,
            'task_id': task_id
        })
    return jsonify(ret), 201 if len(ret) > 0 else 406

@new_tasks.route('/getText', methods=['POST'])
def textTask(*args, **kwargs):
    return handleTaskWrapper(task=TextTask, *args, **kwargs)

@new_tasks.route('/getImages', methods=['POST'])
def imageTask(*args, **kwargs):
    return handleTaskWrapper(task=ImageTask, *args, **kwargs)

@new_tasks.route('/crawlWebsite', methods=['POST'])
def webcrawlTask(*args, **kwargs):
    return handleTaskWrapper(task=WebCrawlTask, *args, **kwargs)
