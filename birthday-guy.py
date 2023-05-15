import os
import csv
import yaml
import time
import pytz
import emoji
import requests
import webbrowser
import sys, threading
from flask import Flask
from datetime import datetime, timedelta

app = Flask(__name__)

threads = list()

@app.route('/')
def hello_world():
    print("hello world")

def start():
    print("STARTED RUNNING FUNCTION 'START()'")
    while 1:
        

        config = yaml.safe_load(open("config.yml"))
        print(config)

        # GroupMe Bot ID
        botID = config["botID"]  # insert your Bot ID here

        # Prefix string before name
        birthdayText = config["postText"]

        # Timezone to start the bot in specific time
        timezone = config["timezone"]

        # Time when the bot starts
        timeStart = config["timeStart"].split(":")

        # List of names with a birthday on the current date
        birthdayBoys = []

        # Current Date
        datetimeObject = datetime.now()
        currentDate = str(datetimeObject.month) + "/" + str(datetimeObject.day+1)
        # currentDate = '12/30' # used for testing (best birthday)

        # defining the object and localising it to a timezone
        obj = datetime.now()
        obj = obj.replace(hour=int(timeStart[0]))
        obj = obj.replace(minute=int(timeStart[1]))
        obj = obj.replace(second=0)
        tz = pytz.timezone('Europe/Dublin')
        obj = tz.localize(obj)
         
        # Creating a new timezone
        new_tz = pytz.timezone(timezone)
         
        # Changing the timezone of our object
        new_tz_time = obj
         
        # Printing out new time
        print(new_tz_time)

        while pytz.timezone('Europe/Dublin').localize(datetime.now()).astimezone(pytz.timezone(timezone)).minute != new_tz_time.minute or pytz.timezone('Europe/Dublin').localize(datetime.now()).astimezone(pytz.timezone(timezone)).hour != new_tz_time.hour:
            print(f"sleeping, time is: hour - {pytz.timezone('Europe/Dublin').localize(datetime.now()).astimezone(pytz.timezone(timezone)).hour} minute - {pytz.timezone('Europe/Dublin').localize(datetime.now()).astimezone(pytz.timezone(timezone)).minute} second - {pytz.timezone('Europe/Dublin').localize(datetime.now()).astimezone(pytz.timezone(timezone)).second}")
            print(f'waiting for: hour - {new_tz_time.hour} minute - {new_tz_time.minute} ')
            time.sleep(60)

        # Turn birthday-list.csv into a dictionary and create a list of birthday bois
        with open('birthday-list.csv', mode='r', encoding="utf-8-sig") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if row['Birthday'] == currentDate:
                    birthdayBoys += {row['Full Name']}

        # get last names of the birthday bois
        lastNames = []
        if len(birthdayBoys) == 1:
            split = birthdayBoys[0].split(' ')
            lastNames += split[-1:]
        elif len(birthdayBoys) > 1:
            for boi in birthdayBoys:
                split = boi.split(' ')
                lastNames += split[-1:]

        # construct message text
        postText = ''
        if len(birthdayBoys) == 1:
            postText = emoji.emojize(birthdayText + birthdayBoys[0])
        elif len(birthdayBoys) > 1:
            for i, name in enumerate(birthdayBoys):
                if i != (len(birthdayBoys) - 1):
                    postText += emoji.emojize(birthdayText + name + '\n\n')
                else:
                    postText += emoji.emojize(birthdayText + name)

        # construct and send the post
        postData = {'bot_id': botID,
                    'text': postText}

        r = requests.post('https://api.groupme.com/v3/bots/post', json=postData)
        print(r)

        #print(f"sleeping, time is: hour - {pytz.timezone('Europe/Dublin').localize(datetime.now()).astimezone(pytz.timezone(timezone)).hour} minute - {pytz.timezone('Europe/Dublin').localize(datetime.now()).astimezone(pytz.timezone(timezone)).minute}")
        #print(f'waiting for: hour - {new_tz_time.hour} minute - {new_tz_time.minute} ')
        time.sleep(60)


#@app.before_first_request(start)

def run_app():
    port = int(os.environ.get("PORT", 5000))
    #print("trying to run before first request funcs")
    #print(app.before_first_request_funcs)
    #print("finished running before first request funcs")
    #webbrowser.open(f'http://localhost:{port}')
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    y = threading.Thread(target=run_app)
    threads.append(y)
    y.start()
    x = threading.Thread(target=start)
    threads.append(x)
    x.start()
