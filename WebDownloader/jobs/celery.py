from pathlib import Path

from celery import Celery

from WebDownloader.core.config import Config
from WebDownloader.jobs.tasks import ImageTask, TextTask


class CeleryClient(object):
    """
        Celery with app specified configuration
    """
    _celery: Celery
    textTask: TextTask

    imageTask: ImageTask

    def __init__(self, config: Config, **kwargs):
        # save config & create celery
        self.config = config
        self._celery = Celery(__name__, broker=self.config['BROKER_URL'], backend=self.config['CELERY_RESULT_BACKEND'],
                              **kwargs)

        # register tasks
        self.textTask = self.celery.register_task(TextTask(self.config))
        self.imageTask = self.celery.register_task(ImageTask(self.config))

    @property
    def celery(self):
        """celery property
        :return: celery instance
        """
        return self._celery

    def check_state(self, task_id: str):
        """Checks task's state
        Because all tasks are PENDING by default, it's replaced with SENT,
        (PENDING means NOT FOUND)

        :param task_id: task's id
        :return: task's status
        """
        status = self.celery.AsyncResult(task_id).status
        return status

    def find_result(self, task_id: str) -> str:
        """Specifies name of result file

        :param task_id: task's id
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

