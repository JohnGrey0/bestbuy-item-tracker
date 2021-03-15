# bestbuy-item-tracker
This was created to track out of stock items from best buy and notify me via text when anything is restocked.

Logical steps of the program
1) Send request to api
2) Check response for in stock products
3) Notify user via text for each in stock product
4) Repeat every 10 seconds until items are in stock then sleep for 10 minutes

# Python module requirements
```python3 -m pip install -r requirements.txt```
- Twilio
- Requests

# Twilio requirements
https://www.twilio.com/
- Phone number
- SID
- Auth Token

# Bestbuy requirements
https://developer.bestbuy.com/
- API Key

# Environment variables needed if you wish to use it as-is.
Add to your zprofile/bash_profile/windows environment before using.
- TWILIO_FROM_NUMBER="+##########"
- TWILIO_ACCOUNT_SID="<YOUR_SID>"
- TWILIO_AUTH_TOKEN="<YOUR_AUTH_TOKEN>
- MY_PHONE="+##########"
- BEST_BUY_API_TOKEN="<BESTBUY_API_TOKEN>

# Usage
The items are hardcoded in an dictionary as the url is super long. You will have to modify the list for different products.
- python -m main -i "3070"
- python -m main -i "3080"
- python -m main -i "xbox"

<img width="1291" alt="Screen Shot 2021-03-15 at 1 19 56 PM" src="https://user-images.githubusercontent.com/46507986/111194088-3623cc80-8591-11eb-97c2-ead39b77f31c.png">
