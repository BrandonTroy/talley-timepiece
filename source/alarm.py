from datetime import datetime
from threading import Event
from time import sleep, time
import os


class Alarm:
    counter = 0
    current = None
    audio_file_path = "audio/mixkit-rooster-crowing-in-the-morning-2462.wav"
    
    def __init__(self, _time: datetime, days: list, active: bool):
        self.time = _time
        self.days = days
        self.active = active
        self.snoozed = False
        self.going_off = False
        self.index = Alarm.counter
        Alarm.counter += 1
        self._snooze_event = Event()
        self._stop_event = Event()
        self.last_gone_off: float = 0
    
    @staticmethod
    def from_json(json: dict):
        """Converts a json object to an Alarm object.
        input format:
        {
            'time': 'HH:MM',
            'days': [0, 1, 2, 3, 4, 5, 6],
            'active': True/False
        }
        """
        return Alarm(
            datetime.strptime(json['time'], "%H:%M"),
            [0, 1, 2, 3, 4, 5, 6],   # set active for all days
            json['active']
        )
    
    def go_off(self):
        """Plays the alarm sound 10 times or until:
            * snoozed - waits snooze_duration and then calls this method again
            * stopped - breaks out of the method and stops the alarm    
        """       
        self.last_gone_off = time()
        # if an alarm is already going off do nothing, or if an alarm is snoozed replace it
        if Alarm.current:
            if Alarm.current.going_off:
                return
            if Alarm.current is not self:
                Alarm.current.stop()
        # start alarm
        Alarm.current = self
        for i in range(30):
            # check for stop
            if self._stop_event.is_set():
                self._stop_event.clear()
                if Alarm.current is self:
                    Alarm.current = None
                self.snoozed = False
                self.going_off = False
                return
            # check for snooze
            if self._snooze_event.is_set():
                self._snooze_event.clear()
                self.snoozed = True
                self.going_off = False
                sleep(5)
                self.snoozed = False
                self.go_off()
                break
            self.going_off = True
            # play audio
            os.system("aplay", Alarm.audio_file_path)
            self.going_off = False
        Alarm.current = None
    
    def snooze(self):
        """Sets the snooze event which is checked in the go_off method and snoozes the alarm"""
        self._snooze_event.set()
        
    def stop(self):
        """Sets the snooze event which is checked in the go_off method and stops the alarm"""
        self._stop_event.set()
        self.snoozed = False
    
    def compare_time(self, _time: datetime):
        """Returns True if the time matches the alarm time in minute and hour and if
            the current day of the week is in the alarm's days list"""
        return (
            _time.weekday() in self.days and
            self.time.hour == _time.hour and 
            self.time.minute == _time.minute
        )
    
    def __eq__(self, other):
        return self.time == other.time and self.days == other.days and self.active == other.active
    
    def __lt__(self, other):
        return self.time < other.time
    
    def __gt__(self, other):
        return self.time > other.time
    
    def __str__(self):
        return f"A{self.index + 1}: {'SNZ' if self.snoozed else 'ON' if self.active else 'OFF'}"
    
    def __hash__(self):
        return hash(str(self))
    
    def __repr__(self):
        return repr(str(self))
    
    def __del__(self):
        self.stop()