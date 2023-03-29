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





import os, threading

event = threading.Event()

def play():
    for i in range(10):
        if event.is_set(): break
        os.system("aplay audio.wav")



audio_thread = threading.Thread(target=play)
audio_thread.start()


input("press enter to stop")
event.set()