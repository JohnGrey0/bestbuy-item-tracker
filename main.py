import argparse
import requests
import time
import re
from random import randint
from datetime import datetime
from os import system, name, getenv
from twilio.rest import Client
from sys import exit


def send_text(message):
    client = Client(getenv("TWILIO_ACCOUNT_SID"),
                    getenv("TWILIO_AUTH_TOKEN"))
    message = client.messages.create(
        body=message,
        from_=getenv("TWILIO_FROM_NUMBER"),
        to=getenv("MY_PHONE"),
    )


def api_token_shuffle():
    tokens = [
        getenv("BEST_BUY_API_TOKEN_1"),
        getenv("BEST_BUY_API_TOKEN_2")
    ]
    return tokens[randint(0, 1)]


def get_product_info_from_api(url):
    success_code = 200
    url = url.format(api_key=api_token_shuffle())
    response = requests.get(url)
    status_code = response.status_code
    if status_code == success_code:
        return response.json().get("products", None), status_code
    return None, status_code


def get_product_list(url):
    status_code = 0
    products = None
    counter = 0
    max_retries = 24
    sleep = 300
    while status_code != 200 and products is None and counter < max_retries:
        counter += 1
        try:
            print("{} - Checking products for availability attempt #{}...".format(str(datetime.now()), counter))
            products, status_code = get_product_info_from_api(url)
            if products is None:
                time.sleep(30)
        except Exception as e:
            time.sleep(sleep)
    return products


def items_are_stocked(products):
    is_stocked = False
    for product in products:
        message = "{name}\nAdd to cart: {addToCartUrl}\n${salePrice}\nURL: {url}".format(**product)
        print("{0:115} - {1:8} - {2:40} [{3:8}]".format(
            product["name"],
            "$"+str(product["salePrice"]),
            product["addToCartUrl"],
            "IN STOCK" if product["onlineAvailability"] else "OUT OF STOCK")
            )
        if product["onlineAvailability"]:
            send_text(message)
            is_stocked = True
    return is_stocked


def change_delay():
    start = 9
    end = 13
    current_hour = datetime.now().hour
    return 2 if start <= current_hour <= end else 20

# https://api.bestbuy.com/v1/products((search=RTX&search=30)&categoryPath.id=abcat0507002&salePrice>100&salePrice<3000)?apiKey={api_key}&sort=onlineAvailability.asc&show=name,salePrice,addToCartUrl,onlineAvailability,url&pageSize=100&format=json
# https://api.bestbuy.com/v1/products((search=RTX&search=30)&categoryPath.id=abcat0507002&salePrice>100&salePrice<1200)?apiKey={api_key}&sort=onlineAvailability.asc&show=name,salePrice,addToCartUrl,onlineAvailability,url&pageSize=100&format=json
# nohup python3 -um main -u "https://api.bestbuy.com/v1/products((search=RTX&search=30)&categoryPath.id=abcat0507002&salePrice>100&salePrice<1200)?apiKey={api_key}&sort=onlineAvailability.asc&show=name,salePrice,addToCartUrl,onlineAvailability,url&pageSize=100&format=json" &
def main():
    parser = argparse.ArgumentParser(description="which product to look for")
    parser.add_argument("-u", "--url", type=str, help="url")
    args = parser.parse_args()
    url = args.url if args.url else None

    if url is None:
        print("URL argument is not added. Please add.")
        exit()

    delay_if_stocked = 900
    while True:
        delay = change_delay()
        products = get_product_list(url)
        if items_are_stocked(products):
            print("Items are stocked. Sleeping...")
            time.sleep(delay_if_stocked)
        else:
            print("No items are in stock. Rechecking in {} seconds...".format(delay))
            time.sleep(delay)

if __name__ == "__main__":
    main()