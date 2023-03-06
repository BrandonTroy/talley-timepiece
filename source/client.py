from time import sleep
from datetime import datetime
import pytz
from threading import Thread
from alarm import Alarm
from requests import get
from json import loads

from colored import fg, attr


class App:
    SERVER_URL = 'https://talley-timepiece.vercel.app'
    timezone = 'America/New_York'
    alarms: list[Alarm] = []

    def start():
        Thread(target=App.fetch, daemon=True).start()
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
            result = get(App.SERVER_URL + '/api/pi')
            print(fg(10), "REQUEST: ", result, attr('reset'), sep="")
            
            data = loads(result.text)
            print(fg(39), data, attr('reset'), sep="")
            App.timezone = data['timezone']
            App.alarms = list(map(Alarm.from_json, data['alarms']))
            
            sleep(3)


if __name__ == '__main__':
    App.start()