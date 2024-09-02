import requests
from bs4 import BeautifulSoup
import re


class Crawler:
    def get_definition(self, word: str):
        pass


class CrawlerFR(Crawler):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    def __init__(self):
        self.base_url = 'https://dictionnaire.lerobert.com/definition/{word}'

    def get_definition(self, word: str):
        request_url = self.base_url.replace('{word}', word)
        print('Crawling ', request_url, '...')
        page = requests.get(request_url, headers=self.headers)
        soup_handler = BeautifulSoup(page.content, 'html.parser')
        # get the definition elements with css classes 'd_dvn' or 'd_dfn'
        definition_elts = soup_handler.select('.d_dvn, .d_dfn')
        definitions = [elt.text for elt in definition_elts]
        definition = '\n\n'.join(definitions) if definitions else 'NOT_FOUND'
        # remove extra new lines
        definition = re.sub(r'(\n\s*)+\n+', '\n\n', definition) if definition else None
        print('definition:', definition)
        return definition


class CrawlerEN(Crawler):

    def __init__(self):
        self.base_url = 'https://www.dictionary.com/browse/{word}'

    def get_definition(self, word: str):
        request_url = self.base_url.replace('{word}', word)
        page = requests.get(request_url)
        soup_handler = BeautifulSoup(page.content, 'html.parser')
        selector = '#top-definitions > div:nth-child(1) > section.q7ELwPUtygkuxUXXOE9t.LVt92HnYuY17Vv04474m'
        definition_elt = soup_handler.select_one(selector)
        return re.sub(r'(\n\s*)+\n+', '\n\n', definition_elt.text) if definition_elt else None
