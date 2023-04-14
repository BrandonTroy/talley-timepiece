import RPi.GPIO as GPIO 
from time import sleep


pins = (18, 22, 24, 26)   # 4 GPIO pins which are motor inputs
steps = 200   # number of steps per revolution of the motor
tick_steps = 10   # number of steps per (half) tick of the motor
delay = 1 / (2 * tick_steps)   # delay between steps 


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
    sleep(delay)
    
# takes one step (two half steps) clockwise
def clockwise_step():
    step(0, 0, 0, 1)
    step(1, 0, 0, 1)
    step(1, 0, 0, 0)
    step(1, 0, 1, 0)
    step(0, 0, 1, 0)
    step(0, 1, 1, 0)
    step(0, 1, 0, 0)
    step(0, 1, 0, 1)

# takes one step (two half steps) counter clockwise
def counter_clockwise_step():
    step(0, 1, 0, 1)
    step(0, 1, 0, 0)
    step(0, 1, 1, 0)
    step(0, 0, 1, 0)
    step(1, 0, 1, 0)
    step(1, 0, 0, 0)
    step(1, 0, 0, 1)
    step(0, 0, 0, 1)


try:
    # shift motor half of a tick left to put it in centered position
    for i in range(tick_steps // 2):
        clockwise_step()
    
    # infinitely repeat the four step pattern to rotate the motor
    while True:
        for i in range(tick_steps):
            counter_clockwise_step()
            
        for i in range(tick_steps):
            clockwise_step()
            
except KeyboardInterrupt:
    # clean up pins
    step(0, 0, 0, 0)