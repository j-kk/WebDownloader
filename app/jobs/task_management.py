from pathlib import Path
from . import module


def check_state(task_id: str):
    status = module.celery.AsyncResult(task_id).status
    if status == 'PENDING':
        status = 'NOT FOUND'
    return status


def find_result(task_id: str):
    db = module.config['DATA_LOCATION']
    file = db.joinpath(Path(task_id))
    if file.with_suffix('.txt').exists():
        return task_id.join('.txt')
    elif file.with_suffix('.zip').exists():
        return task_id.join('.zip')
    else:
        return None
