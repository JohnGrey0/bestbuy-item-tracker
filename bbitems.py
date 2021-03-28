import requests
import time
from datetime import datetime
from helpers import api_token_shuffle, send_to_discord
from os import getenv


class BBStock():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_product_info_from_api(self, url):
        success_code = 200
        url = url.format(api_key=api_token_shuffle())
        response = requests.get(url)
        status_code = response.status_code
        if status_code == success_code:
            return response.json().get("products", None), status_code
        return None, status_code

    def get_product_list(self, url):
        status_code = 0
        products = None
        counter = 0
        max_retries = 24
        sleep = 30
        while status_code != 200 and products is None and counter < max_retries:
            counter += 1
            try:
                print("{} - Bestbuy - Checking products for availability attempt #{}...".format(str(datetime.now()), counter))
                products, status_code = self.get_product_info_from_api(url)
                if products is None:
                    time.sleep(sleep)
            except Exception as e:
                time.sleep(sleep)
        return products

    def bestbuy_items_stocked(self, products):
        is_stocked = False
        for product in products:
            url = getenv("DISCORD_BB_HOOK")
            message = """
This item seems to be in stock!\n
**{name}**\n
SKU: {sku}\n
Price: ${salePrice}\n
URL: {url}\n
Add to Cart: {addToCartUrl}""".format(**product)
            if product["onlineAvailability"]:
                send_to_discord(url, message)
                is_stocked = True
        return is_stocked

    def process(self, url):
        products = self.get_product_list(url)
        return self.bestbuy_items_stocked(products)
