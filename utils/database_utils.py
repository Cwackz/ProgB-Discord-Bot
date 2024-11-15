import sqlite3
import os
from bcrypt import hashpw, gensalt, checkpw

DATABASE_PATH = "logs.db"

def create_database():
    """Creates the database and tables if they do not exist."""
    if not os.path.exists(DATABASE_PATH):
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
            """)

            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()

def create_user(username: str, password: str) -> bool:
    """Creates a new user with a hashed password in the database."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone() is not None:
            return False 
        
        password_hash = hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()

def login_user(username: str, password: str) -> bool:
    """Validates username and password against stored hashed password."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result is None:
            return False 
        
        user_id, password_hash = result
        
        if checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            cursor.execute("INSERT OR REPLACE INTO sessions (user_id, username) VALUES (?, ?)", (user_id, username))
            conn.commit()
            return True
        return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()

def logout_user(user_id: int) -> bool:
    """Logs out a user by removing their session."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()

def is_user_logged_in(user_id: int) -> bool:
    """Checks if a user is logged in based on their session."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM sessions WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        return result is not None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()

create_database()
