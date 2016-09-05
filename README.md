LaundryView Notification Script
===============================

Get notified when washers and dryers in your favorite laundry room become available.

I wrote this while I was waiting for a laundry room in Simmons Hall to open up.

# Installation

```
pip install -r requirements.txt
```

# Configuration

Put your Yo API key and username in a .env file (see .env.example for an example).
You can also put the room IDs of the rooms you want to check by default (so you don't
have to enter them as command line arguments each time you start the script).

# Running

To continuously check rooms 1364825 and 1364826 to see if one of them has 1 washer
and 1 dryer available for 3 consecutive minutes, run: 

```
./check.py -w 1 -d 1 -t 3 1364825 1364826
```

the script will continue checking every 1 minute.  As soon as one of the rooms has
the mininmum numberof washers and dryers available for the specified number of minutes,
it will print out on the command line and send you a "Yo" to notify you a room is available.

