import bcrypt

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
