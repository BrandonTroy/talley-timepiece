from datetime import datetime


class Alarm:   
    def __init__(self, _time: datetime, days: str, active: bool):
        self.time = _time
        self.days = days
        self.active = active
    
    @staticmethod
    def from_json(json: dict):
        return Alarm(
            datetime.strptime(json['time'], "%H:%M:%S"),
            json['days'],
            json['active']
        )
    
    def go_off(self):
        # TODO: send audio file to the speaker and emit noise
        print("Alarm is going off")
    
    def __eq__(self, other):
        return self.time == other.time and self.days == other.days and self.active == other.active
    
    def __lt__(self, other):
        return self.time < other.time
    
    def __gt__(self, other):
        return self.time > other.time
    
    def __str__(self):
        return f"{self.time} {self.days} {self.active}"
    
    def __hash__(self):
        return hash(str(self))
    
    def __repr__(self):
        return repr(str(self))