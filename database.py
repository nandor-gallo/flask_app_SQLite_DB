import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute(
    'CREATE TABLE students (sid TEXT, first TEXT, last TEXT, dob TEXT, amount TEXT)')

print("Table created successfully")
conn.close()
