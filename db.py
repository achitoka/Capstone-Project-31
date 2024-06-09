import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Koneksi ke database berhasil.")
        create_table(conn)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            print("Database ditutup.")

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        print("Tabel users berhasil dibuat.")
    except sqlite3.Error as e:
        print(e)

if __name__ == '__main__':
    create_connection("user.db")
