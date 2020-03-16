import re
import validators
import requests
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup

CONNECT_TIMEOUT=5.0
READ_TIMEOUT=15.0

def get_url(url: str) -> str:
    url = re.sub('\n', '', url)
    if not re.match('http://', url) and not re.match('https://', url):
        url = 'http://' + url
    return url

def is_correct(url: str):
    return validators.url(url)

class WebImage(object):
    url: str
    response: requests.Response

    def __init__(self, url: str):
        self.url = url

    def download(self, dir_path: Path):
        # if path doesn't exist, make that path dir
        if not dir_path.parent.is_dir():
            dir_path.parent.mkdir(parents=True)
        # download the body of response by chunk, not immediately
        response = requests.get(self.url, stream=True, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT))

        # get the total file size
        file_size = int(response.headers.get("Content-Length", 0))

        # get the file name
        filename = dir_path.joinpath(Path(self.url.split("/")[-1]))


        # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8196):
                if chunk: #filter out keep-alive chunks
                    file.write(chunk)


class Website(object):
    url: str
    response: requests.Response
    soup: BeautifulSoup

    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
    ]

    def __init__(self, url: str):
        self.url = url

    def download(self):
        self.url = get_url(self.url)
        self.response = requests.get(self.url, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT))
        self.soup = BeautifulSoup(self.response.text, "html.parser")


    def extractTextFromWebsite(self):
        for script in self.soup(['script', 'style']):
            script.extract()

        text = self.soup.get_text()

        lines = (line.strip() for line in text.splitlines())

        chunks = (phrase.strip() for line in lines for phrase in line.split(' '))

        text = ' '.join(chunk for chunk in chunks if chunk)

        return text

    def getTitle(self) -> str:
        """Searches for webpage's title
            If title is not found, it generates one from url
        :return: webpage title's
        """
        try:
            fragment = re.search(r"<title(.|\s)+?</title>", self.response.text)[0]
            title = re.sub(r"<(/)?title>", "", fragment)
        except IndexError:
            title = self.url.replace('/', '_').replace('.', '_').replace(':', '')
        return title

    def getImages(self) -> [WebImage]:
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
            if is_correct(img_url):
                images.append(WebImage(img_url))
        return images
