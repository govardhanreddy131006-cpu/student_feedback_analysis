import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="govardhan@#2024",
        database="college_db"
    )