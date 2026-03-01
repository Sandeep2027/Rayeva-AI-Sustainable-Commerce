# ==================== database.py ====================
import sqlite3
import os
from datetime import datetime

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/database.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        ai_output TEXT,
        created_at TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS proposals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        budget REAL,
        ai_output TEXT,
        created_at TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS impacts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_summary TEXT,
        ai_output TEXT,
        created_at TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        module TEXT,
        input TEXT,
        output TEXT
    )""")
    conn.commit()
    conn.close()

def log_interaction(module: str, input_data: dict, output_data: dict):
    conn = sqlite3.connect("data/database.db")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "INSERT INTO logs (timestamp, module, input, output) VALUES (?, ?, ?, ?)",
        (ts, module, str(input_data), str(output_data))
    )
    conn.commit()
    conn.close()

def get_recent_logs(limit=10):
    conn = sqlite3.connect("data/database.db")
    cursor = conn.execute(
        "SELECT timestamp, module, input, output FROM logs ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    logs = cursor.fetchall()
    conn.close()
    return logs

