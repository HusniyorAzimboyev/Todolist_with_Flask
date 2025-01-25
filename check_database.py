import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM todo")
print(cursor.fetchall())