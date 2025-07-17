# utils/init_db.py

import sqlite3

def initialize():
    conn = sqlite3.connect("your_database.db")  # adjust the path if needed
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS course (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subject (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY(course_id) REFERENCES course(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS topic (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY(subject_id) REFERENCES subject(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS topic_content (
        topic_id INTEGER PRIMARY KEY,
        reference_text TEXT,
        content_text TEXT,
        image_urls TEXT,
        slide_deck_md TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(topic_id) REFERENCES topic(id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize()
    print("Database initialized.")
