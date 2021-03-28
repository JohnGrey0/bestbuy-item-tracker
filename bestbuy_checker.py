import time
import logging
from helpers import change_delay
from bbitems import BBStock


def bestbuy_notify():
    delay_if_stocked = 30
    url = "https://api.bestbuy.com/v1/products((search=RTX&search=30)&categoryPath.id=abcat0507002&salePrice>100)?apiKey={api_key}&sort=onlineAvailability.dsc&show=sku,name,salePrice,addToCartUrl,onlineAvailability,url&pageSize=100&format=json"
    bb_obj = BBStock()
    while True:
        delay = change_delay()
        products = bb_obj.get_product_list(url)
        if bb_obj.bestbuy_items_stocked(products):
            print("Items are stocked! Repeating every 30 seconds...")
            time.sleep(delay_if_stocked)
        else:
            print("No items are in stock. Rechecking in {} seconds...".format(delay))
            time.sleep(delay)

if __name__ == "__main__":
    bestbuy_notify()