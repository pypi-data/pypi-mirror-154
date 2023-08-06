import requests
from bs4 import BeautifulSoup
import re
from urllib.request import Request, urlopen


class Scpr:
    def __init__(self,url):
        self.url = url
    def get_info(self):
        req = Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        info = BeautifulSoup(webpage,"html.parser")
        links1 = [link["href"] for link in info.find_all('a',href=re.compile("/pdf/"))]
        return links1
