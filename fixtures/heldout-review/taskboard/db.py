import sqlite3

_conn = None


def conn():
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(":memory:")
        _conn.row_factory = sqlite3.Row
        _conn.executescript(
            "CREATE TABLE tasks(id INTEGER PRIMARY KEY, project TEXT, title TEXT, owner TEXT, due TEXT, done INTEGER DEFAULT 0);"
        )
    return _conn


def add_task(project, title, owner, due=None):
    c = conn()
    cur = c.execute("INSERT INTO tasks(project, title, owner, due) VALUES (?, ?, ?, ?)", (project, title, owner, due))
    c.commit()
    return cur.lastrowid
