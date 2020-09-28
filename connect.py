import mysql.connector
from mysql.connector import Error


def connect():
    """ Connect to MySQL database """
    conn = None
    try:
        conn = mysql.connector.connect(host='lineup499.mysql.database.azure.com',
                                       database='clup',
                                       user='admin499',
                                       password='CS499class')
        if conn.is_connected():
            print('Connected to MySQL database')

    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


if __name__ == '__main__':
    connect()


import mysql.connector

mydb = mysql.connector.connect(
  host="lineup499.mysql.database.azure.com",
  user="admin499",
  password="CS499class"
)

print(mydb)

print("Hello World!")
