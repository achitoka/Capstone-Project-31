import sqlite3

def create_connection():
       try:
           conn = sqlite3.connect('dbtomat.db')  # Sesuaikan dengan database yang Anda gunakan
           return conn
       except sqlite3.Error as e:
           print(e)
           return None

