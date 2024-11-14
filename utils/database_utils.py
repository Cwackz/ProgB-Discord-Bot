import sqlite3
import os
from datetime import datetime

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "../database/logs.db")

def create_tables():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                content TEXT NOT NULL
            )"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS command_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command_name TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                channel_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )"""
        )
        conn.commit()

def log_command(command_name: str, user_id: int, channel_id: int):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO command_logs (command_name, user_id, channel_id, timestamp) VALUES (?, ?, ?, ?)",
            (command_name, user_id, channel_id, timestamp)
        )
        conn.commit()

def get_command_logs(limit: int = 100):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM command_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
        return cursor.fetchall()


create_tables()
