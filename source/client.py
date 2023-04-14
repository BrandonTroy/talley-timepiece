from time import sleep, time
from datetime import datetime, timedelta
import pytz
from threading import Thread
from alarm import Alarm
from requests import get, post
from json import loads
import drivers
import RPi.GPIO as GPIO



BUTTON_PIN = 37

# initialze the GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    
class App:
    SERVER_URL = 'https://talley-timepiece.vercel.app'
    timezone = 'America/New_York'
    alarms: list[Alarm] = [
        Alarm.from_json(['00:00', None, False]),
        Alarm.from_json(['00:00', None, False])
    ]
    display = drivers.Lcd()

    # initializes app and starts threads
    @staticmethod
    def start():
        Thread(target=App.fetch, daemon=True).start()
        Thread(target=App.input_listener, daemon=True).start()
        App.tick()
    
    # updates the time every second based on the timezone
    @staticmethod
    def tick():
        while True:
            t = datetime.now(pytz.timezone(App.timezone))
            # check for alarm needing to go off
            for alarm in App.alarms:
                if alarm.active and alarm.compare_time(t) and (time() - alarm.last_gone_off) >= 60:
                    Thread(target=alarm.go_off, daemon=True).start()
            # update the display
            time_string = datetime.strftime(t, "%I:%M %p")
            alarm_string = "  ".join(map(str, App.alarms))
            App.display.lcd_display_string(time_string.center(16), 1)
            App.display.lcd_display_string(alarm_string.center(16), 2)
            sleep(1)
    
    # fetches the app data from the server
    @staticmethod
    def fetch():
        while True:
            result = get(App.SERVER_URL + '/api/pi')
            data = loads(result.text)
            App.timezone = data['timezone']
            Alarm.audio_file_path = 'audio/' + data['sound']
            Alarm.counter = 0
            # update alarms only if they have changed
            for i, alarm in enumerate(map(Alarm.from_json, data['alarms'])):
                if alarm != App.alarms[i]:
                    App.alarms[i].stop()
                    App.alarms[i] = alarm
            # check for snooze or stop from server
            if Alarm.current:
                if data['stop']:
                    Alarm.current.stop()
                elif data['snooze']:
                    Alarm.current.snooze()
            print("REQUEST:", result)
            print(data)
            sleep(1)
    
    # listens for local input, specifically button presses
    @staticmethod
    def input_listener():
        while True:
            # wait for button down press (rising edge)
            while GPIO.input(37) == GPIO.LOW:
                sleep(0.1)
            # process button press
            if Alarm.current:
                if Alarm.current.snoozed:
                    Alarm.current.stop()
                    post(App.SERVER_URL + '/stop')
                else:
                    Alarm.current.snooze()
                    post(App.SERVER_URL + '/snooze')
            # wait for button up press (falling edge)
            while GPIO.input(37) == GPIO.HIGH:
                sleep(0.1)
            


if __name__ == '__main__':
    try:
        App.start()
    except KeyboardInterrupt:
        GPIO.cleanup()