#!/bin/bash

# Check if gedit is running
# -x flag only match processes whose name (or command line if -f is
# specified) exactly match the pattern. 

if pgrep -x "lulu" > /dev/null
then
    echo "Running"
else
    echo "Stopped"
    nohup python3 -um /Desktop/git/bestbuy-item-tracker/lulu &
fi

if pgrep -x "bestbuy_checker" > /dev/null
then
    echo "Running"
else
    echo "Stopped"
    nohup python3 -um /Desktop/git/bestbuy-item-tracker/bestbuy_checker &
fi
