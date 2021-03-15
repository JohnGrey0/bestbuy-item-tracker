# bestbuy-item-tracker
This was created to track out of stock items from best buy and notify me via text when anything is restocked.

# Requirements
- Python 3
- Twilio
- Bestbuy API token

# Environment variables needed if you wish to use it as-is.
Add to your zprofile/bash_profile/windows environment before using.
- TWILIO_FROM_NUMBER="+##########"
- TWILIO_ACCOUNT_SID="<YOUR_SID>"
- TWILIO_AUTH_TOKEN="<YOUR_AUTH_TOKEN>
- BEST_BUY_API_TOKEN="<BESTBUY_API_TOKEN>

# Usage
The items are hardcoded in an dictionary as the url is super long. You will have to modify the list for different products.
- python -m main -i "3070"
- python -m main -i "3080"
- python -m main -i "xbox"

![bestbuy_tracker copy](https://user-images.githubusercontent.com/46507986/111192981-0de79e00-8590-11eb-8df9-c7d5874a3b3f.gif)
