import RPi.GPIO as GPIO 
from time import sleep


class Motor:
    def __init__(self, pins: tuple[int, int, int, int], rpm: int, steps: int = 200, mode: GPIO.Mode = GPIO.BOARD):
        GPIO.setmode(mode)
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
        self.pins = pins
        self.rpm = rpm
        self.steps = steps
        
    def step(self, a, b, c, d):
        GPIO.output(self.pins[0], a)
        GPIO.output(self.pins[1], b)
        GPIO.output(self.pins[2], c)
        GPIO.output(self.pins[3], d)
        
    def rotate(self, steps: int = None):
        if steps is None:
            steps = self.steps
        delay = 60 / self.steps / self.rpm
        for i in range(steps // 4):
            self.step(0, 1, 0, 1)
            sleep(delay)
            self.step(0, 1, 1, 0)
            sleep(delay)
            self.step(1, 0, 1, 0)
            sleep(delay)
            self.step(1, 0, 0, 1)
            sleep(delay)
            
    def perpetuate(self):
        while True:
            self.rotate()