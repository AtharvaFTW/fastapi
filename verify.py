import sqlite3
conn = sqlite3.connect("your_database.db")
rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
print(rows)
