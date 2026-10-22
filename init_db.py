# init_db.py
import sqlite3
from werkzeug.security import generate_password_hash
import os

DB_PATH = 'reports.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        latitude REAL,
        longitude REAL,
        category TEXT,
        date_reported TEXT,
        status TEXT DEFAULT 'pending',
        image_path TEXT
    );
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT
    );
    ''')
    conn.commit()
    conn.close()
    print("Database initialized:", DB_PATH)

def seed_admin(username='admin', password='admin123'):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    pw_hash = generate_password_hash(password)
    try:
        c.execute("INSERT INTO admins (username, password_hash) VALUES (?, ?)", (username, pw_hash))
        conn.commit()
        print(f"Admin user created: {username} / {password}")
    except Exception as e:
        print("Admin already exists or error:", e)
    conn.close()

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        init_db()
    else:
        print("DB already exists:", DB_PATH)
    seed_admin()