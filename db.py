
import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="77492652Rt@",
        database="student_management"
    )
