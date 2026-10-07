import sqlite3

DB_FILE = "WeakSpot.db"


def connect():
    return sqlite3.connect(DB_FILE)


def create_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id      INTEGER PRIMARY KEY,
            time    INTEGER NOT NULL,
            verdict TEXT,
            problem TEXT NOT NULL,
            name    TEXT NOT NULL,
            rating  INTEGER
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS submission_tags (
            submission_id INTEGER NOT NULL,
            tag           TEXT NOT NULL,
            PRIMARY KEY (submission_id, tag),
            FOREIGN KEY (submission_id) REFERENCES submissions(id)
        )
    """)
    conn.commit()


def save_submissions(conn, submissions):
    for s in submissions:
        conn.execute(
            "INSERT OR IGNORE INTO submissions VALUES (?, ?, ?, ?, ?, ?)",
            (s["id"], s["time"], s["verdict"], s["problem"], s["name"], s["rating"]),
        )
        for tag in s["tags"]:
            conn.execute(
                "INSERT OR IGNORE INTO submission_tags VALUES (?, ?)",
                (s["id"], tag),
            )
    conn.commit()