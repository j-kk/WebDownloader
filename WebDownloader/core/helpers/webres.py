import time
import furl
from pathlib import Path
from urllib.parse import urljoin
import networkx as nx
import queue
import requests
import validators
from bs4 import BeautifulSoup

CONNECT_TIMEOUT = 5.0
READ_TIMEOUT = 15.0

class WebImage(object):
    """Representation of image on website

    """
    url: str
    response: requests.Response

    def __init__(self, url: str):
        self.url = url

    def download(self, dir_path: Path):
        """Downloads image and saves in specified location

        :param dir_path: image location
        """
        # if path doesn't exist, make that path dir
        if not dir_path.parent.is_dir():
            dir_path.parent.mkdir(parents=True)
        # download the body of response by chunk, not immediately
        response = requests.get(self.url, stream=True, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT))

        # get the file name
        filename = dir_path.joinpath(Path(self.url.split("/")[-1][:32]))

        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8196):
                if chunk:  # filter out keep-alive chunks
                    file.write(chunk)


class Website(object):
    """Representation of website, with possibility to extract images & text

    """
    url: str
    response: requests.Response
    soup: BeautifulSoup

    def __init__(self, url: str):
        self.url = url

    def download(self):
        """Downloads and parses website content

        """
        self.url = get_url(self.url)
        self.response = requests.get(self.url, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT))
        self.soup = BeautifulSoup(self.response.text, "html.parser")

    def extractTextFromWebsite(self) -> str:
        """Extracts text from already downloaded website

        :return: website text
        """
        for script in self.soup(['script', 'style']):
            script.extract()

        text = self.soup.body.get_text()

        lines = (line.strip() for line in text.splitlines())

        chunks = (phrase.strip() for line in lines for phrase in line.split(' '))

        text = ' '.join(chunk for chunk in chunks if chunk)

        return text

    def getImages(self) -> [WebImage]:
        """Extracts images from websites

        :return: list of image properties
        """
        images = []
        for img in self.soup.find_all("img"):
            img_url = img.attrs.get("src")
            if not img_url:
                # if img does not contain src attribute, just skip
                continue
            img_url = urljoin(self.url, img_url)
            # remove URLs like '/hsts-pixel.gif?c=3.2.5'
            try:
                pos = img_url.index("?")
                img_url = img_url[:pos]
            except ValueError:
                pass
            # finally, if the url is valid
            if validators.url(img_url):
                images.append(WebImage(img_url))
        return images

    def createLinkMap(self, depth) -> nx.Graph:
        G = nx.Graph()
        visited = set(self.url)
        q = queue.Queue()
        q.put((self, 0))
        G.add_node(self.url)
        while not q.empty():
            website, site_depth = q.get()
            try:
                website.download()
            except requests.exceptions.InvalidURL as exc:
                print(f'Invalid url {website.url}, error: {exc}')
                continue
            except requests.exceptions.ConnectionError as exc:
                time.sleep(2)
                print(f'Max retries! Link: {website.url}, error: {exc}')
                q.put((self, site_depth))
                continue
            links = website.extractLinksFromWebsite()
            for link in links:
                if link.endswith('pdf'):
                    continue
                if link not in visited:
                    visited.add(link)
                    if site_depth < depth:
                        website = Website(link)
                        q.put((website, site_depth + 1))
                    G.add_node(link)
                    G.add_edge(website.url, link)
        return G

    def extractLinksFromWebsite(self) -> [str]:
        try:
            raw_links = self.soup.find_all('a')
            links = list(map(lambda link: link.get('href'), raw_links))
            links = filter(lambda link: type(link) == str, links)
            complete_links = map(lambda link: link if link.startswith(('http', 'https', 'www')) else urljoin(self.url, link), links)
            return map(lambda link: furl.furl(link).remove(args=True, fragment=True).url, complete_links)
        except Exception as err:
            raise err
