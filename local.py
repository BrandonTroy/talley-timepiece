from time import sleep
from datetime import datetime
import pytz
from threading import Thread
from alarm import Alarm
from requests import get
from json import loads

class App:
    SERVER_URL = 'http://localhost:5000'
    timezone = 'America/New_York'
    alarms: list[Alarm] = []

    def start():
        App.tick()
    
    # updates the time every second based on the timezone
    def tick():
        while True:
            t = datetime.now(pytz.timezone(App.timezone))
            print(str(t.time())[:8])
            sleep(1)
    
    # fetches the app data from the server
    def fetch():
        while True:
            result = loads(get(App.SERVER_URL).text)
            App.timezone = result['timezone']
            App.alarms = list(map(Alarm.from_json, result['alarms']))
            sleep(3)


if __name__ == '__main__':
    App.start()