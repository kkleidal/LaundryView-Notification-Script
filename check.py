#!/usr/bin/env python

import requests
import re
import time
import os
import argparse
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def get_rooms():
    return (int(room) for room in os.environ.get("ROOMS").split(","))

def get_link(room):
    return "http://classic.laundryview.com/laundry_room.php?view=c&lr=%d" % room

def get_html(room):
    r = requests.get(get_link(room))
    assert(r.status_code == 200)
    return r.text

number_regex = re.compile(ur'WASHERS:</span>\s*(\d+) of \d+ available\s*<span[^>]*>DRYERS:</span>\s*(\d+) of \d+ available')
def number_available(room):
    html = get_html(room)
    match = re.search(number_regex, html)
    return { "washer": int(match.group(1)), "dryer": int(match.group(2)) }

def available(room, min_washers=1, min_dryers=1):
    number = number_available(room)
    return number["washer"] >= min_washers and number["dryer"] >= min_dryers

def yo(room):
    r = requests.post("http://api.justyo.co/yo/", data={
        'api_token': os.environ.get("YO_API_KEY"),
        'username': os.environ.get("YO_RECIPIENT_USERNAME"),
        'link': get_link(room),
        'text': "laundry room available"
    })
    if r.status_code < 400:
        print "Sent a yo about %d" % room 
    else:
        print "An error occurred while sending a yo about %d" % room 

AVAIL_FOR_X_MINUTES = 3
def main(washers, dryers, rooms, minutes):
    history = {};
    yoed = set();
    while True:
        for room in rooms:
            if available(room, min_washers=washers, min_dryers=dryers):
                history[room] = history.get(room, 0) + 1
                if history[room] >= AVAIL_FOR_X_MINUTES:
                    print "%d is available!" % room
                    if room not in yoed:
                        yoed.add(room)
                        yo(room)
            else:
                history[room] = 0
        time.sleep(60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get yo\'ed when a washers and driers are available')
    parser.add_argument('rooms', metavar='rooms', type=int, nargs='*',
                               help='the ids of the laundry rooms (the lr parameter in the URL of LaundryView). If none are provided, looks for the ROOMS env variable for a comma separated list.', default=list(get_rooms()))
    parser.add_argument('-w', '--washers', dest='washers', type=int, nargs='?', help="the minimum number of washers available to consider a room available", default=1) 
    parser.add_argument('-d', '--dryers', dest='dryers', type=int, nargs='?', help="the minimum number of dryers to consider a room available", default=1) 
    parser.add_argument('-t', '--time-available-before-notification', dest='minutes', type=int, nargs='?', help="the number of minutes the room must be available before sending a notification", default=3) 
    args = parser.parse_args()
    main(**vars(args))
