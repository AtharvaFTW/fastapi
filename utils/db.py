# utils/db.py

import sqlite3

DB_FILE = "your_database.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    schema = """
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        course_id INTEGER NOT NULL,
        FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        subject_id INTEGER NOT NULL,
        FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS topic_content (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_id INTEGER NOT NULL UNIQUE,
        reference_text TEXT,
        content_text TEXT,
        image_urls TEXT,
        slide_deck_md TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
    );
    """
    with get_connection() as conn:
        conn.executescript(schema)

def fetch_courses():
    with get_connection() as conn:
        return conn.execute("SELECT id, name FROM courses ORDER BY name").fetchall()

def fetch_subjects(course_id):
    with get_connection() as conn:
        return conn.execute(
            "SELECT id, name FROM subjects WHERE course_id = ? ORDER BY name", (course_id,)
        ).fetchall()

def fetch_topics(subject_id):
    with get_connection() as conn:
        return conn.execute(
            "SELECT id, name FROM topics WHERE subject_id = ? ORDER BY name", (subject_id,)
        ).fetchall()

def add_course(name):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM courses WHERE lower(name) = ?", (name.lower(),))
        if cur.fetchone():
            return False, "Already exists, add new data or continue to next step"
        cur.execute("INSERT INTO courses (name) VALUES (?)", (name,))
        conn.commit()
        return True, "Course added successfully"

def add_subject(name, course_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id FROM subjects WHERE lower(name) = ? AND course_id = ?",
            (name.lower(), course_id)
        )
        if cur.fetchone():
            return False, "Already exists, add new data or continue to next step"
        cur.execute(
            "INSERT INTO subjects (name, course_id) VALUES (?, ?)",
            (name, course_id)
        )
        conn.commit()
        return True, "Subject added successfully"

def add_topic(name, subject_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id FROM topics WHERE lower(name) = ? AND subject_id = ?",
            (name.lower(), subject_id)
        )
        if cur.fetchone():
            return False, "Already exists, add new data or continue to next step"
        cur.execute(
            "INSERT INTO topics (name, subject_id) VALUES (?, ?)",
            (name, subject_id)
        )
        conn.commit()
        return True, "Topic added successfully"
