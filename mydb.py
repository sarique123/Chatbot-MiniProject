import mysql.connector

dataBase = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    user = 'root',
    passwd='ABC@123#abc@',
)

# Prepare a cursor object
cursorObject: object = dataBase.cursor()

# Create database
cursorObject.execute('CREATE DATABASE IF NOT EXISTS chatbot')
print("ALL DONE!")