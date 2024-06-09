import sqlite3
import bcrypt

# Konfigurasi koneksi ke database SQLite
db_config = 'dbtomat.db'  # Nama file database SQLite

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
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            conn.close()
            return True
    except sqlite3.Error as err:
        print(f"Error: {err}")
    return False

def verify_user(username, password):
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            conn.close()
            if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
                return True
    except sqlite3.Error as err:
        print(f"Error: {err}")
    return False

# Buat tabel pengguna saat modul diimpor
create_user_table()
