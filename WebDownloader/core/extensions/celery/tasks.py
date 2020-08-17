import shutil

import networkx as nx
import matplotlib.pyplot as plt

from . import cc
from core.helpers.webres import Website
from core.config import config

@cc.celery.task
def TextTask(site_url: str, *args, **kwargs):
    """
    :param self: api property
    :param site_url: url to website
    """
    # download website
    website = Website(url=site_url)
    website.download()
    # and save to file
    output_name = TextTask.request.id + '.txt'
    output_location = config['DATA_LOCATION'].joinpath(output_name)
    with open(output_location, 'w') as file:
        file.write(website.extractTextFromWebsite())
    return output_name


@cc.celery.task
def ImageTask(site_url: str, *args, **kwargs):
    """Downloads all images from website and saves them to zip archive

    :param self: api property
    :param site_url: url to website
    """
    # download website
    website = Website(url=site_url)
    website.download()

    # create temporary catalog to save images
    dir_path = config['DATA_LOCATION'].joinpath(ImageTask.request.id)
    dir_path.mkdir()

    # download images
    images = website.getImages()
    for image in images:
        image.download(dir_path)

    # pack to zip and remove tmp catalog
    zip_path = config['DATA_LOCATION'].joinpath(str(ImageTask.request.id))
    zip_filename = str(ImageTask.request.id) + '.zip'
    shutil.make_archive(zip_path, 'zip', config['DATA_LOCATION'], str(ImageTask.request.id))
    shutil.rmtree(dir_path)
    return zip_filename

@cc.celery.task
def WebCrawlTask(self, site_url: str, depth: int = 1, *args, **kwargs):
    website = Website(url=site_url)
    G = website.createLinkMap(depth)
    nx.draw(G, with_labels=False)
    filename = str(WebCrawlTask.request.id) + '.png'
    filepath = config['DATA_LOCATION'].joinpath(filename)
    plt.savefig(filepath)
    return filename

