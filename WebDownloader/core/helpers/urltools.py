import re

def get_url(url: str) -> str:
    """Adds http prefix to url if not present

    :param url: url to website
    :return: url with http prefix
    """
    url = re.sub('\n', '', url)
    if not re.match('http://', url) and not re.match('https://', url):
        url = 'http://' + url
    return url