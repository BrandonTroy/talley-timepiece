# import mysql.connector
# db_connection = mysql.connector.connect(
#   host="sql111.epizy.com",
#   user="epiz_33736479",
#   passwd="Jx0TaR2JSeV",
#   database="epiz_33736479_talleytimepiece",
#   port=3306
# )
# my_database = db_connection.cursor()
# my_database.execute("SELECT * FROM TIMEZONE")
# output = my_database.fetchall()
# print(output)


# # won't connect to database
# import pymysql
# connection = pymysql.connect(
#   host="talley-timepiece.cqizwwsi7lin.us-east-1.rds.amazonaws.com",
#   user="admin",
#   passwd="password",
#   database="talley-timepiece",
#   port=3306
# )
# with connection:
#   cur = connection.cursor()
#   cur.execute("SELECT VERSION()")
#   version = cur.fetchone()
#   print("Database version: {} ".format(version[0]))


# from requests import get
# import time
# from json import loads


# while True:
#     result = get('https://talley-timepiece.vercel.app/api/pi')
#     data = loads(result.text)
#     print("REQUEST:", result)
#     print(data)
#     time.sleep(0.5)


# import RPi.GPIO as GPIO

# GPIO.setwarnings(False) # Ignore warning for now
# GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
# GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input>

# while True: # Run forever
#     if GPIO.input(37) == GPIO.HIGH:
#         print("Button was pushed!")




# A = 18
# B = 22
# C = 24
# D = 26

# GPIO.setup(A, GPIO.OUT)
# GPIO.setup(B, GPIO.OUT)
# GPIO.setup(C, GPIO.OUT)
# GPIO.setup(D, GPIO.OUT)

# def step(a, b, c, d):
#     GPIO.output(A, a)
#     GPIO.output(B, b)
#     GPIO.output(C, c)
#     GPIO.output(D, d)


# import time
# steps = 200
# delay = 2/steps

# while True:
#     for i in range(0, steps//4):
#         step(0, 1, 0, 1)
#         time.sleep(delay)
#         step(0, 1, 1, 0)
#         time.sleep(delay)
#         step(1, 0, 1, 0)
#         time.sleep(delay)
#         step(1, 0, 0, 1)
#         time.sleep(delay)
        
        
        
        
        
from threading import Thread, Event
from os import system
from time import sleep
import RPi.GPIO as GPIO



snooze = Event()
stop = Event()

def go_off():
    for i in range(10):
        if snooze.is_set():
            snooze.clear()
            sleep(5)
            if not stop.is_set():
                go_off()
            stop.clear()
            break
        system("aplay audio.wav")



GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



def pressed():
    print("BUTTON PRESSED")
    if snooze.is_set():
        stop.set()
    else:
        snooze.set()


Thread(target=go_off, daemon=True).start()

try:
    # wait for button down press (rising edge)
    while GPIO.input(37) == GPIO.LOW:
        pass
    
    pressed()
    
    # wait for button up press (falling edge)
    while GPIO.input(37) == GPIO.HIGH:
        pass
except KeyboardInterrupt:
    GPIO.cleanup()