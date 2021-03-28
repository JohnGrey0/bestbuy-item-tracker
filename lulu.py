from scraper import Scraper
from os import getenv
from helpers import send_to_discord
import time

def lulu_notify(url):
    tag = "button"
    data = {"data-lulu-track": "pdp-add-to-bag-regular-enabled"}
    scrape = Scraper()
    item_html = scrape.get_item_html(url)
    in_stock = scrape.check_item_in_stock(item_html, tag, data)
    if in_stock:
        hook_url = getenv("DISCORD_LULU_HOOK")
        # hook_url = getenv("DISCORD_TEST_HOOK")
        title = scrape.get_page_attributes(item_html, tag="div", data={"itemprop":"name"}, index=0)
        price = scrape.get_page_attributes(item_html, tag="span", data={"class":"price-1SDQy price"}, index=2)
        katie_id = "<@670486749461348372>"
        message = "{id}\n**{title}**\t-\tIN STOCK!\nPrice: ${price}\nURL: {url}".format(id=katie_id, title=title, price=price, url=url)
        send_to_discord(hook_url, message)
    return in_stock


if __name__ == "__main__":
    urls = [
            "https://shop.lululemon.com/p/women-pants/Align-Pant-Tall/_/prod9410067?color=26950&sz=12",
            # "https://shop.lululemon.com/p/women-pants/Align-Pant-Tall/_/prod9410067?color=26950&sz=0",
            # "https://shop.lululemon.com/p/women-pants/Align-Pant-Tall/_/prod9410067?color=26950&sz=2",
            # "https://shop.lululemon.com/p/mens-sweatpants/Balancer-Pant-27/_/prod10370080?color=47780&sz=XL",
            # "https://shop.lululemon.com/p/mens-sweatpants/Balancer-Pant-27/_/prod10370080?color=46696&sz=XL",
            # "https://shop.lululemon.com/p/men-pants/Commission-Pant-Classic-Warpstreme-28-US/_/prod10390085?color=43731&sz=38",
            # "https://shop.lululemon.com/p/men-pants/Commission-Pant-Classic-Warpstreme-28-US/_/prod10390085?color=32476&sz=38"
        ]
    while True:
        for url in urls:
            lulu_notify(url)
        print("Lulu - Sleeping for 10 minutes.")
        time.sleep(600)
