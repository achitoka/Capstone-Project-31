import sqlite

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

if __name__ == '__main__':
    create_user_table()
