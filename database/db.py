import sqlite3
from pathlib import Path
from datetime import date
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Create data folder automatically
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "study_tracker.db"


def get_connection():
    return sqlite3.connect(DB_PATH)
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        topic TEXT NOT NULL,
        date TEXT NOT NULL,
        completed INTEGER DEFAULT 0,
        planned INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        topic TEXT NOT NULL,
        minutes INTEGER NOT NULL,
        date TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        current_percent INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mock_tests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_name TEXT,
        score INTEGER,
        test_date TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS revisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        r1 INTEGER DEFAULT 0,
        r2 INTEGER DEFAULT 0,
        r3 INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def add_task(subject, topic, task_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks(subject, topic, date) VALUES (?, ?, ?)",
        (subject, topic, task_date)
    )

    conn.commit()
    conn.close()


def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, subject, topic, completed
    FROM tasks
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()
    return data


def complete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET completed=1 WHERE id=?",
        (task_id,)
    )

    conn.commit()
    conn.close()


def get_total_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]

    conn.close()
    return total


def get_completed_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM tasks
    WHERE completed=1
    """)

    completed = cursor.fetchone()[0]

    conn.close()
    return completed


def add_study_session(subject, topic, minutes, study_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO study_sessions
    (subject, topic, minutes, date)
    VALUES (?, ?, ?, ?)
    """, (subject, topic, minutes, study_date))

    conn.commit()
    conn.close()


def get_total_study_minutes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COALESCE(SUM(minutes),0)
    FROM study_sessions
    """)

    total = cursor.fetchone()[0]

    conn.close()
    return total


def get_all_sessions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT subject, topic, minutes, date
    FROM study_sessions
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()
    return data


def add_planned_task(subject, topic, task_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tasks
    (subject, topic, date, planned)
    VALUES (?, ?, ?, 1)
    """, (subject, topic, task_date))

    conn.commit()
    conn.close()


def get_planned_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, subject, topic
    FROM tasks
    WHERE planned=1
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()
    return data


def add_topic(subject, topic):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO progress(subject, current_percent)
    VALUES (?, 0)
    """, (f"{subject}:{topic}",))

    conn.commit()
    conn.close()


def get_topics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, subject, current_percent
    FROM progress
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()
    return data


def complete_topic(topic_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT subject
    FROM progress
    WHERE id=?
    """, (topic_id,))

    row = cursor.fetchone()

    if row:

        topic_name = row[0]

        cursor.execute("""
        UPDATE progress
        SET current_percent=100
        WHERE id=?
        """, (topic_id,))

        cursor.execute("""
        SELECT id
        FROM revisions
        WHERE topic=?
        """, (topic_name,))

        exists = cursor.fetchone()

        if not exists:

            cursor.execute("""
            INSERT INTO revisions(topic)
            VALUES(?)
            """, (topic_name,))

    conn.commit()
    conn.close()


def add_mock_test(test_name, score, test_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO mock_tests(test_name, score, test_date)
    VALUES (?, ?, ?)
    """, (test_name, score, test_date))

    conn.commit()
    conn.close()


def get_mock_tests():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mock_tests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_name TEXT,
        score INTEGER,
        test_date TEXT
    )
    """)

    cursor.execute("""
    SELECT test_name, score, test_date
    FROM mock_tests
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()
    return data


def add_revision(topic):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO revisions(topic)
    VALUES (?)
    """, (topic,))

    conn.commit()
    conn.close()


def get_revisions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS revisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        r1 INTEGER DEFAULT 0,
        r2 INTEGER DEFAULT 0,
        r3 INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    SELECT id, topic, r1, r2, r3
    FROM revisions
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()
    return data


def update_revision(revision_id, revision_no):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"UPDATE revisions SET r{revision_no}=1 WHERE id=?",
        (revision_id,)
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database created successfully!")

def add_revision_if_not_exists(topic):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id
    FROM revisions
    WHERE topic=?
    """, (topic,))

    exists = cursor.fetchone()

    if not exists:

        cursor.execute("""
        INSERT INTO revisions(topic)
        VALUES(?)
        """, (topic,))

    conn.commit()
    conn.close()

def get_completed_topics_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM progress
    WHERE current_percent=100
    """)

    total = cursor.fetchone()[0]

    conn.close()
    return total


def get_total_topics_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM progress
    """)

    total = cursor.fetchone()[0]

    conn.close()
    return total


def get_pending_revisions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM revisions
    WHERE r3=0
    """)

    total = cursor.fetchone()[0]

    conn.close()
    return total


def get_latest_mock_score():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT score
    FROM mock_tests
    ORDER BY id DESC
    LIMIT 1
    """)

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return 0
def get_completed_topics_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM progress
    WHERE current_percent=100
    """)

    total = cursor.fetchone()[0]

    conn.close()
    return total


def get_total_topics_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM progress
    """)

    total = cursor.fetchone()[0]

    conn.close()
    return total


def get_pending_revisions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM revisions
    WHERE r3=0
    """)

    total = cursor.fetchone()[0]

    conn.close()
    return total


def get_latest_mock_score():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT score
    FROM mock_tests
    ORDER BY id DESC
    LIMIT 1
    """)

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return 0