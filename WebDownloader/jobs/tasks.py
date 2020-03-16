import shutil

from celery.signals import after_task_publish

from . import module
from WebDownloader.core.helpers.webres import Website

celery = module.celery

@after_task_publish.connect
def update_sent_state(sender=None, headers=None, **kwargs):
    """
        Updates task when it's sent to mark it is created
        (because celery by default does not distinguish pending and not existing tasks)
    """
    task = celery.tasks.get(sender)
    backend = task.backend if task else celery.backend
    backend.store_result(headers['id'], None, "SENT")


@celery.task(bind=True)
def textTask(self, site_url: str):
    """Downloads all text from website
    :param self: task property
    :param site_url: url to website
    """
    # download website
    website = Website(url=site_url)
    website.download()
    # and save to file
    output_name = module.config['DATA_LOCATION'].joinpath(self.request.id + '.txt')
    with open(output_name, 'w') as file:
        file.write(website.extractTextFromWebsite())


@celery.task(bind=True)
def imageTask(self, site_url: str):
    """Downloads all images from website and saves them to zip archive

    :param self: task property
    :param site_url: url to website
    """
    # download website
    website = Website(url=site_url)
    website.download()

    # create temporary catalog to save images
    dir_path = module.config['DATA_LOCATION'].joinpath(self.request.id)
    dir_path.mkdir()

    # download images
    images = website.getImages()
    for image in images:
        image.download(dir_path)

    # pack to zip and remove tmp catalog
    zip_path = module.config['DATA_LOCATION'].joinpath(self.request + '.zip')
    shutil.make_archive(zip_path, 'zip', dir_path)
    shutil.rmtree(dir_path)
