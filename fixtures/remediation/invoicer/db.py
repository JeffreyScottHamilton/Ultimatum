import sqlite3

SCHEMA = """
CREATE TABLE tenants (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id),
    name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'member',
    token TEXT NOT NULL UNIQUE
);
CREATE TABLE invoices (
    id INTEGER PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id),
    customer TEXT NOT NULL,
    amount_cents INTEGER NOT NULL,
    created TEXT NOT NULL,
    notes TEXT NOT NULL DEFAULT ''
);
"""


def connect():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn
