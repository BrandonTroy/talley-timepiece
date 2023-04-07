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


import RPi.GPIO as GPIO

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input>

while True: # Run forever
    if GPIO.input(37) == GPIO.HIGH:
        print("Button was pushed!")


#GPIO.setup(12, GPIO.OUT)
#while True:
#       GPIO.output(12, GPIO.LOW)

#p = GPIO.PWM(12, 100)
#p.start(1)
