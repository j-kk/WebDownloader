from API import factory
from API.resources.websiteProcessors import Website
from celery.signals import after_task_publish


celery = factory.celery

@after_task_publish.connect
def update_sent_state(sender=None, headers=None, **kwargs):
    task = celery.tasks.get(sender)
    backend = task.backend if task else celery.backend

    backend.store_result(headers['id'], None, "SENT")

@celery.task(bind=True)
def textTask(self, site_url: str):
    website = Website(url= site_url)
    website.download()
    output_name = factory.flask.config['DATA_LOCATION'].joinpath(website.getTitle()+'.txt')
    with open(output_name, 'w') as file:
        file.write(website.extractTextFromWebsite())



