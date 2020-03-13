import re
import requests


class Website(object):
    url: str
    response: requests.Response

    def __init__(self, url: str):
        self.url = url

    def download(self):
        self.url = self._get_url()
        self.response = requests.get(self.url)

    def _get_url(self):
        url = re.sub('\n', '', self.url)
        if not re.match('http://', url) and not re.match('https://', url):
            url = 'http://' + url
        return url

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
