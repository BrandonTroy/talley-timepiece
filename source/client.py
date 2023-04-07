from time import sleep, time
from datetime import datetime, timedelta
import pytz
from threading import Thread
from alarm import Alarm
from requests import get
from json import loads
import drivers
import RPi.GPIO as GPIO


# initialze the GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


class App:
    SERVER_URL = 'https://talley-timepiece.vercel.app'
    timezone = 'America/New_York'
    alarms: list[Alarm] = []
    display = drivers.Lcd()

    @staticmethod
    def start():
        Thread(target=App.fetch, daemon=True).start()
        Thread(target=App.input_listener, daemon=True).start()
        App.alarms = []
        App.tick()
    
    # updates the time every second based on the timezone
    @staticmethod
    def tick():
        while True:
            t = datetime.now(pytz.timezone(App.timezone))
            
            for alarm in App.alarms:
                if alarm.active and alarm.compare_time(t) and (time() - alarm.last_gone_off) >= 60:
                    Thread(target=alarm.go_off, daemon=True).start()
            
            time_string = datetime.strftime(t, "%I:%M:%S %p")
            alarm_string = "  ".join(map(str, App.alarms))
            App.display.lcd_display_string(time_string, 1)
            App.display.lcd_display_string(alarm_string, 2)
            sleep(1)
    
    # fetches the app data from the server
    @staticmethod
    def fetch():
        while True:
            result = get(App.SERVER_URL + '/api/pi')
            data = loads(result.text)
            App.timezone = data['timezone']
            Alarm.counter = 0
            App.alarms = list(map(Alarm.from_json, data['alarms']))
            print("REQUEST:", result)
            print(data)
            sleep(3)
    
    # listens for local input, specifically button presses
    @staticmethod
    def input_listener():
        while True:
            # wait for button down press
            while GPIO.input(12) == GPIO.LOW:
                pass
            # wait for button up press
            while GPIO.input(12) == GPIO.HIGH:
                pass
            if Alarm.current:
                if Alarm.current.snoozed:     # type: ignore
                    Alarm.current.stop()      # type: ignore
                else:
                    Alarm.current.snooze()    # type: ignore


if __name__ == '__main__':
    App.start()