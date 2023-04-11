import RPi.GPIO as GPIO 
from time import sleep


pins = (18, 22, 24, 26)   # 4 GPIO pins which are motor inputs
steps = 200   # number of steps per revolution of the motor
rpm = 30   # desired revolutions per minute
delay = 60 / steps / rpm   # delay between steps 

# setup the GPIO pins
GPIO.setmode(GPIO.BOARD)
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

# sets the state of the four input pins
def step(a, b, c, d):
    GPIO.output(pins[0], a)
    GPIO.output(pins[1], b)
    GPIO.output(pins[2], c)
    GPIO.output(pins[3], d)

try:
    # infinitely repeat the four step pattern to rotate the motor
    while True:
        step(0, 1, 0, 1)
        sleep(delay)
        step(0, 1, 1, 0)
        sleep(delay)
        step(1, 0, 1, 0)
        sleep(delay)
        step(1, 0, 0, 1)
        sleep(delay)
except KeyboardInterrupt:
    # clean up pins
    step(0, 0, 0, 0)