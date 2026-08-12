import sqlite3
import os

DB_FILE = "users.db"

def init_db():
    # Reset DB every time
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    users = [
        ("admin", "admin123"),
        ("student", "password123"),
        ("guest", "guest123"),
        ("test", "test123")
    ]

    c.executemany(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        users
    )

    conn.commit()
    conn.close()

    print("✅ DB Initialized")

if __name__ == "__main__":
    init_db()
