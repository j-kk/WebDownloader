import re
from urllib.parse import urljoin
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_url(url: str) -> str:
    url = re.sub('\n', '', url)
    if not re.match('http://', url) and not re.match('https://', url):
        url = 'http://' + url
    return url



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
        response = requests.get(self.url, stream=True)

        # get the total file size
        file_size = int(response.headers.get("Content-Length", 0))

        # get the file name
        filename = dir_path.joinpath(Path(self.url.split("/")[-1]))


        # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
        progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            for data in progress:
                f.write(data)
                progress.update(len(data))



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
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, "html.parser")


    def extractTextFromWebsite(self):
        text = re.sub("\n", '', self.response.text)
        text = re.sub(r"<script(.|\s)+?</script>", '', text)
        text = re.sub('<.*?>', ' ', text)
        text = re.sub(r"<style(.|\s)+?</style>", '', text)
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
        for img in tqdm(self.soup.find_all("img"), "Extracting images"):
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