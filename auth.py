import bcrypt
import sqlite3

db_config = 'dbtomat.db'
# Fungsi untuk membuat koneksi ke database SQLite
def get_db_connection():
    try:
        conn = sqlite3.connect(db_config)
        return conn
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None

def create_user_table():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

def add_user(username, password):
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            # Cek apakah username sudah ada
            cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
            if cursor.fetchone():
                print("Username already exists.")
                return False
            
            # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            print("User added successfully.")
            return True
    except sqlite3.Error as err:
        print(f"Error: {err}")
    finally:
        if conn:
            conn.close()
    return False

def verify_user(username, password):
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
                print("User verified successfully.")
                return True
            else:
                print("Invalid username or password.")
    except sqlite3.Error as err:
        print(f"Error: {err}")
    finally:
        if conn:
            conn.close()
    return False
