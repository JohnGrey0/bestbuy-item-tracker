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
        return response.json().get("products", None)
    return None


def is_item_stocked(url):
    products = get_product_info_from_api(url)
    anything_stocked = False
    if products is not None:
        products = sorted(products, key=lambda k: k['salePrice'])
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
    valid_items = ["3070", "3080", "xbox"]
    items = {
        "3080": "https://api.bestbuy.com/v1/products((search=RTX&search=3080)&categoryPath.id=abcat0507002)?apiKey={api_key}&sort=onlineAvailability.asc&show=addToCartUrl,accessories.sku,onlineAvailability,salePrice,regularPrice,mobileUrl,name&pageSize=100&format=json",
        "3070": "https://api.bestbuy.com/v1/products((search=RTX&search=3070)&categoryPath.id=abcat0507002)?apiKey={api_key}&sort=onlineAvailability.asc&show=addToCartUrl,accessories.sku,onlineAvailability,salePrice,regularPrice,mobileUrl,name&pageSize=100&format=json",
        "xbox": "https://api.bestbuy.com/v1/products(sku=6428324)?apiKey={api_key}&sort=onlineAvailability.asc&show=onlineAvailability,addToCartUrl,mobileUrl,name,salePrice&format=json"
    }

    item = args.item if args.item else None

    url = items[item] if item in valid_items else None

    if url is not None:
        while True:
            print(datetime.now(), "- Checking availability of items...")
            if not is_available:
                is_available = is_item_stocked(url)
            else:
                print("Items were available. Sleeping for 10 minutes")
                time.sleep(600)
            print("Sleeping for 10 seconds")
            time.sleep(10)
            clear_screen()
    else:
        print("Invalid item choice. Please fix.")
