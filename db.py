import sqlite3

def create_connection():
       try:
           conn = sqlite3.connect('database.db')  # Sesuaikan dengan database yang Anda gunakan
           return conn
       except sqlite3.Error as e:
           print(e)
           return None

def verify_user(username, password):
       conn = create_connection()
       if conn is None:
           raise AttributeError("Failed to create database connection.")
       cursor = conn.cursor()
       # Lanjutkan dengan query untuk memverifikasi pengguna

