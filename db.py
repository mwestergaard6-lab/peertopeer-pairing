import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "peertopeer.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enforce foreign keys in SQLite
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    conn = get_conn()
    cur = conn.cursor()

    # Students table: role = 'mentor' or 'mentee'
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('mentor', 'mentee')),
        subject TEXT NOT NULL
    );
    """)

    # Pairs table: mentor + mentee reference students.id
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pairs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mentor_id INTEGER NOT NULL,
        mentee_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        FOREIGN KEY (mentor_id) REFERENCES students(id) ON DELETE CASCADE,
        FOREIGN KEY (mentee_id) REFERENCES students(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()
