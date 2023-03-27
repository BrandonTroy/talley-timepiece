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





import pygame

pygame.mixer.init()
sound = pygame.mixer.Sound('small-audio.mp3')
volume = 0.5

for i in range(3):
  sound.set_volume(volume)
  playing = sound.play()
  while playing.get_busy():
    pygame.time.delay(100)
  volume += 0.25

print("sound over")