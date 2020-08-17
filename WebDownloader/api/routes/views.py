from flask import Blueprint, send_from_directory, request, jsonify
from api.schemas.tasks import TaskIdSchema
from api import redis, celery

task_view = Blueprint('task_view', __name__)


@task_view.route('/checkState', methods=['POST'])
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
        if redis.exists(task_id) == 0:
            continue
        status = celery.check_state(task_id)
        metadata = redis.hgetall(task_id)
        ret.append({
            'task_id': task_id,
            'state': status,
            'time': metadata['time'],
            'type': metadata['type'],
        })
        if status == 'SUCCESS':
            ret[-1]['filename'] = celery.get_result_name(task_id)
    return jsonify(ret), 201 if len(ret) > 0 else 404


@task_view.route('/downloadResults/<filename>')
def get(filename):
    """Returns api result
    :return: api result
    """
    return send_from_directory(task_view.static_folder, filename)  # TODO replace becouse it's slow
