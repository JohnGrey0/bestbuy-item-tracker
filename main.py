import argparse
import requests
import time
from datetime import datetime
from os import system, name, getenv
from twilio.rest import Client


def send_text(message):
    client = Client(getenv("TWILIO_ACCOUNT_SID"),
                    getenv("TWILIO_AUTH_TOKEN"))
    message = client.messages.create(
        body=message,
        from_=getenv("TWILIO_FROM_NUMBER"),
        to=getenv("MY_PHONE"),
    )


def get_product_info_from_api(url):
    url = url.format(api_key=getenv("BEST_BUY_API_TOKEN"))
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("products", None), response.status_code
    return None, response.status_code


def is_item_stocked(url):
    status_code = 0
    products = None
    try:
        products, status_code = get_product_info_from_api(url)
    except Exception as e:
        print("Something went wrong, going to retry again{}".format(e))
    
    if status_code != 200:
        for i in range(0, 4):
            try:
                print("Trying to get product info... Retry #{n}".format(n=i))
                products, status_code = get_product_info_from_api(url)
                if status_code == 200:
                    break
                else:
                    print("Sleeping for 20 minutes")
                    time.sleep(1200)
            except Exception as e:
                print("Something went wrong, going to retry again{}".format(e))
    anything_stocked = False
    if products is not None:
        for product in products:
            print("{0:110} - {1:8} - {2:40} [{3:8}]".format(product["name"], "$"+str(product["salePrice"]),
                                                            product["addToCartUrl"], "IN STOCK" if product["onlineAvailability"] else "OUT OF STOCK"))
            if product["onlineAvailability"]:
                message = "{name}\nAdd to cart: {addToCartUrl}\n${salePrice}\nURL: {mobileUrl}".format(
                    **product)
                send_text(message)
                anything_stocked = True
    return anything_stocked


def clear_screen():
    if name == 'nt':
        _ = system('cls')
    # for mac and linux os(The name is posix)
    else:
        _ = system('clear')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="which product to look for")
    parser.add_argument("-i", "--item", type=str, help="product")
    args = parser.parse_args()
    is_available = False
    valid_items = ["3070", "3080", "xbox", "gpus"]
    items = {
        "gpus": "https://api.bestbuy.com/v1/products((search=RTX&search=30)&categoryPath.id=abcat0507002&salePrice>400&salePrice<1000)?apiKey={api_key}&sort=onlineAvailability.dsc&show=name,salePrice,addToCartUrl,onlineAvailability&pageSize=100&format=json",
        "3080": "https://api.bestbuy.com/v1/products((search=RTX&search=3080)&categoryPath.id=abcat0507002)?apiKey={api_key}&sort=onlineAvailability.asc&show=addToCartUrl,accessories.sku,onlineAvailability,salePrice,regularPrice,mobileUrl,name&pageSize=100&format=json",
        "3070": "https://api.bestbuy.com/v1/products((search=RTX&search=3070)&categoryPath.id=abcat0507002)?apiKey={api_key}&sort=onlineAvailability.asc&show=addToCartUrl,accessories.sku,onlineAvailability,salePrice,regularPrice,mobileUrl,name&pageSize=100&format=json",
        "xbox": "https://api.bestbuy.com/v1/products(sku=6428324)?apiKey={api_key}&sort=onlineAvailability.asc&show=onlineAvailability,addToCartUrl,mobileUrl,name,salePrice&format=json"
    }

    item = args.item if args.item else None

    url = items[item] if item in valid_items else None

    if url is not None:
        delay = 10
        calls_per_second = round(1/delay, 2)
        calls_per_minute = round(60/delay, 2)
        max_calls_per_second = 5.0
        max_calls_per_minute = round(50000/1440, 2)
        while True:
            print("{} - Checking availability of items...".format(datetime.now()))
            if not is_available:
                is_available = is_item_stocked(url)
            else:
                print("Items were available. Sleeping for 10 minutes")
                time.sleep(600)
            print("Calls per second - {0}/{1}".format(calls_per_second, max_calls_per_second))
            print("Calls per minute - {0}/{1}".format(calls_per_minute, max_calls_per_minute))
            print("Sleeping for {delay} seconds".format(delay=delay))
            time.sleep(10)
            clear_screen()
    else:
        print("Invalid item choice. Please fix.")
