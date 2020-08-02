import shutil

import networkx as nx
import matplotlib.pyplot as plt
from celery import Task

from WebDownloader.core.helpers.webres import Website
from ..core.config import Config


class ExtendedTask(Task):
    """Task template, with link to app configuration

    """
    config: Config

    def __init__(self, config: Config):
        self.config = config


class TextTask(ExtendedTask):
    """Text download api
        Downloads all text from website
        Requires app configuration
    """

    def __init__(self, config: Config):
        super().__init__(config)

    def run(self, site_url: str, *args, **kwargs):
        """
        :param self: api property
        :param site_url: url to website
        """
        # download website
        website = Website(url=site_url)
        website.download()
        # and save to file
        output_name = self.request.id + '.txt'
        output_location = self.config['DATA_LOCATION'].joinpath(output_name)
        with open(output_location, 'w') as file:
            file.write(website.extractTextFromWebsite())
        return output_name


class ImageTask(ExtendedTask):
    """Images download api
        Downloads all images from website
        Requires app configuration
    """

    def __init__(self, config: Config):
        super().__init__(config)

    def run(self, site_url: str, *args, **kwargs):
        """Downloads all images from website and saves them to zip archive

        :param self: api property
        :param site_url: url to website
        """
        # download website
        website = Website(url=site_url)
        website.download()

        # create temporary catalog to save images
        dir_path = self.config['DATA_LOCATION'].joinpath(str(self.request.id))
        dir_path.mkdir()

        # download images
        images = website.getImages()
        for image in images:
            image.download(dir_path)

        # pack to zip and remove tmp catalog
        zip_path = self.config['DATA_LOCATION'].joinpath(str(self.request.id))
        zip_filename = str(self.request.id) + '.zip'
        shutil.make_archive(zip_path, 'zip', self.config['DATA_LOCATION'], str(self.request.id))
        shutil.rmtree(dir_path)
        return zip_filename


class WebCrawlTask(ExtendedTask):

    def __init__(self, config: Config):
        super().__init__(config)

    def run(self, site_url: str, depth: int = 1, *args, **kwargs):
        website = Website(url=site_url)
        G = website.createLinkMap(depth)
        nx.draw(G, with_labels=False)
        filename = str(self.request.id) + '.png'
        filepath = self.config['DATA_LOCATION'].joinpath(filename)
        plt.savefig(filepath)
        return filename

