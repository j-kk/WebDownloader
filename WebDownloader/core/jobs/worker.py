from WebDownloader.core.config import set_config
from WebDownloader.core.extensions import set_celery, celeryClient

set_config()
set_celery()

celery = celeryClient
