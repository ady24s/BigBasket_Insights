import sqlite3
import os

db_path = os.path.join("database", "bigbasket_bi.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

try:
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("manager", "bigbasket123"))
except sqlite3.IntegrityError:
    print("Manager already exists.")

conn.commit()
conn.close()
