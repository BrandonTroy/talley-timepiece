import mysql.connector
db_connection = mysql.connector.connect(
  host="sql111.epizy.com",
  user="epiz_33736479",
  passwd="Jx0TaR2JSeV",
  database="epiz_33736479_talleytimepiece",
  port=3306
)
my_database = db_connection.cursor()
my_database.execute("SELECT * FROM TIMEZONE")
output = my_database.fetchall()
print(output)