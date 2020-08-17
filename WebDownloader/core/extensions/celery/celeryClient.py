from pathlib import Path

from celery import Celery
from core.config import config, Config


class CeleryClient(object):
    """
        Celery with app specified configuration
    """
    _instance = None

    _celery: Celery

    def __init__(self, config: Config, **kwargs):
        # save config & create celery
        self.config = config
        self._celery = Celery(__name__, broker=self.config['BROKER_URL'], backend=self.config['CELERY_RESULT_BACKEND'],
                              **kwargs)

    @property
    def celery(self):
        """celery property
        :return: celery instance
        """
        return self._celery

    def check_state(self, task_id: str):
        """Checks api's state
        Because all tasks are PENDING by default, it's replaced with SENT,
        (PENDING means NOT FOUND)

        :param task_id: api's id
        :return: api's status
        """
        status = self.celery.AsyncResult(task_id).status
        return status

    # OBSOLETE
    def find_result(self, task_id: str) -> str:
        """Specifies name of result file

        :param task_id: api's id
        :return: name of result file
        """
        db = self.config['DATA_LOCATION']
        file_path = db.joinpath(Path(task_id))
        if file_path.with_suffix('.txt').exists():
            return task_id + '.txt'
        elif file_path.with_suffix('.zip').exists():
            return task_id + '.zip'
        else:
            raise FileNotFoundError('Result file not found')

    def get_result_name(self, task_id: str) -> str:
        return self.celery.AsyncResult(task_id).get()


def set_celery():
    return CeleryClient(config)

cc = set_celery()
