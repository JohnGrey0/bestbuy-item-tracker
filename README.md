# bestbuy-item-tracker
This was created to track out of stock items from best buy and notify me via text when anything is restocked.

Logical steps of the program
1) Send request to api for products
2) Check response for in stock products
3) Notify user via text for each in stock product
4) Repeat every 10 seconds until items are in stock then sleep for 10 minutes

# Python module requirements
```python -m pip install -r requirements.txt```
- Twilio
- Requests

# Twilio requirements
https://www.twilio.com/
- Phone number
- Account SID
- Auth Token

# Bestbuy requirements
https://developer.bestbuy.com/
- API Key

# Environment variables needed if you wish to use it as-is.
Add to your zprofile/bash_profile/windows environment before using.
- TWILIO_FROM_NUMBER="+###########"
- TWILIO_ACCOUNT_SID="<YOUR_SID>"
- TWILIO_AUTH_TOKEN="<YOUR_AUTH_TOKEN>"
- MY_PHONE="+###########"
- BEST_BUY_API_TOKEN_1="<BESTBUY_API_TOKEN>"
- BEST_BUY_API_TOKEN_2="<BESTBUY_API_TOKEN>"

# Usage
- ```python -m main -u "<INSERT_BEST_BUY_QUERY_BUILDER_URL>"```

Please use this url to build your own query - https://bestbuyapis.github.io/bby-query-builder/#/productSearch

To run in the background and with no output

- ```nohup python -m main -u "<INSERT_BEST_BUY_QUERY_BUILDER_URL>" &```

<img width="1291" alt="Screen Shot 2021-03-15 at 1 19 56 PM" src="https://user-images.githubusercontent.com/46507986/111194088-3623cc80-8591-11eb-97c2-ead39b77f31c.png">



# Bestbuy

```cd /home/pi/Desktop/git/bestbuy-item-tracker
Start - nohup python3 -um bestbuy_checker &
Stop - sudo kill $(pgrep -f bestbuy_checker)```

# Lululemon

```cd /home/pi/Desktop/git/bestbuy-item-tracker
Start - nohup python3 -um lulu &
Stop - sudo kill $(pgrep -f lulu)```

