import requests
from twilio.rest import Client
from os import system, name, getenv
from discord import Webhook, RequestsWebhookAdapter, Embed
from random import randint
from datetime import datetime


def get_useragent():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
        "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    ]
    return agents[randint(0, len(agents)-1)]

def send_to_discord(url, message):
    webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
    embed = Embed()
    embed.description = message
    webhook.send(embed=embed)

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

def change_delay():
    start = 9
    end = 13
    current_hour = datetime.now().hour
    return 10 if start <= current_hour <= end else 10