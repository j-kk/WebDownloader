"""Initialization of the task's handler package"""

from WebDownloader.core import module


module.set_celery(include=['WebDownloader.jobs.tasks'])
celery = module.celery
