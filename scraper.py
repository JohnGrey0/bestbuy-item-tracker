import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
from helpers import get_useragent

class Scraper():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_page_html(self, url):
        headers = {
            "User-Agent": get_useragent()}
        page = requests.get(url, headers=headers)
        if page.status_code == 200:
            return page.content, page.status_code
        return None, page.status_code

    def check_item_in_stock(self, page_html, tag, data):
        soup = BeautifulSoup(page_html, 'html.parser')
        out_of_stock_divs = soup.findAll(tag, data)
        return len(out_of_stock_divs) != 0

    def get_page_attributes(self, page_html, tag, data, index):
        soup = BeautifulSoup(page_html, 'html.parser')
        attribute = soup.findAll(tag, data)
        return attribute[0].contents[index]

    def get_item_html(self, url):
        status_code = 0
        page_html = None
        counter = 0
        max_retries = 24
        sleep = 300
        while status_code != 200 and page_html is None and counter < max_retries:
            counter += 1
            try:
                print("{} - Scraper - Checking products for availability attempt #{}...".format(str(datetime.now()), counter))
                page_html, status_code = self.get_page_html(url)
            except Exception as e:
                time.sleep(sleep)
        return page_html