from flask import Blueprint, send_from_directory, request, g

# from WebDownloader.api.schemas import TaskId
from WebDownloader.api.schemas.tasks import TaskIdSchema

task_data = Blueprint('task_data', __name__)


@task_data.route('/checkState', methods=['POST'])
def post():
    """Checks api's states
    :return: tasks states
    """
    ret = []
    schema = TaskIdSchema()
    req_data = schema.load(request.get_json())
    for task_data in req_data:
        task_id = task_data.id
        if task_id == None:
            continue
        if g.redis.exists(task_id) == 0:
            continue
        status = g.celery.check_state(task_id)
        metadata = g.redis.hgetall(task_id)
        ret.append({
            'task_id': task_id,
            'state': status,
            'time': metadata['time'],
            'type': metadata['type'],
        })
        if status == 'SUCCESS':
            ret[-1]['filename'] = g.celery.get_result_name(task_id)
    return ret, 201 if len(ret) > 0 else 404


# class GetResult():
#     """
#     Handles result queries
#     """
#     flaskInstance: Flask
#
#     def __init__(self, celeryClient: CeleryClient, flaskInstance: Flask, **kwargs):
#         self.celeryClient = celeryClient
#         self.flaskInstance = flaskInstance
#         super().__init__()
#
#     def get(self, filename):
#         """Returns api result
#         :return: api result
#         """
#         return send_from_directory(self.flaskInstance.static_folder, filename)  # TODO replace becouse it's slow
