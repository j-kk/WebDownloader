from pathlib import Path
from . import module


def check_state(task_id: str):
    """Checks task's state
    Because all tasks are PENDING by default, it's replaced with SENT,
    (PENDING means NOT FOUND)

    :param task_id: task's id
    :return: task's status
    """
    status = module.celery.AsyncResult(task_id).status
    if status == 'PENDING':
        status = 'NOT FOUND'
    return status


def find_result(task_id: str) -> str:
    """Specifies name of result file

    :param task_id: task's id
    :return: name of result file
    """
    db = module.config['DATA_LOCATION']
    file_path = db.joinpath(Path(task_id))
    if file_path.with_suffix('.txt').exists():
        return task_id + '.txt'
    elif file_path.with_suffix('.zip').exists():
        return task_id + '.zip'
    else:
        raise FileNotFoundError('Result file not found')
