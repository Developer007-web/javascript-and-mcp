"""
database.py — SQLite schema, connection, and initialization
Uses only Python's built-in sqlite3 module. No external dependencies.
"""

import sqlite3
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "school.db"

_conn: sqlite3.Connection | None = None


def get_db() -> sqlite3.Connection:
    """Return a singleton SQLite connection with row_factory set."""
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        _conn.row_factory = sqlite3.Row          # rows behave like dicts
        _conn.execute("PRAGMA journal_mode = WAL")
        _conn.execute("PRAGMA foreign_keys = ON")
        _init_schema(_conn)
    return _conn


def _init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        -- ── Students ─────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS students (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            class       TEXT    NOT NULL,
            section     TEXT    DEFAULT 'A',
            roll_no     TEXT,
            parent_name TEXT    NOT NULL,
            phone       TEXT    NOT NULL,
            alt_phone   TEXT,
            email       TEXT,
            monthly_fee REAL    NOT NULL,
            discount    REAL    DEFAULT 0,
            sibling_id  INTEGER REFERENCES students(id),
            address     TEXT,
            joined_date TEXT    DEFAULT (date('now')),
            is_active   INTEGER DEFAULT 1,
            notes       TEXT
        );

        -- ── Payments ──────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS payments (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id  INTEGER NOT NULL REFERENCES students(id),
            amount      REAL    NOT NULL,
            month       TEXT    NOT NULL,          -- YYYY-MM
            paid_date   TEXT    DEFAULT (date('now')),
            method      TEXT    DEFAULT 'cash',    -- cash|upi|cheque|online
            reference   TEXT,
            recorded_by TEXT    DEFAULT 'admin',
            notes       TEXT
        );

        -- ── Reminders ─────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS reminders (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id  INTEGER NOT NULL REFERENCES students(id),
            message     TEXT    NOT NULL,
            channel     TEXT    DEFAULT 'whatsapp',
            sent_at     TEXT    DEFAULT (datetime('now')),
            status      TEXT    DEFAULT 'pending',
            month       TEXT
        );

        -- ── Interactions / call logs ──────────────────────────────
        CREATE TABLE IF NOT EXISTS interactions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id  INTEGER NOT NULL REFERENCES students(id),
            type        TEXT    NOT NULL,           -- call|whatsapp|meeting|note
            note        TEXT    NOT NULL,
            created_at  TEXT    DEFAULT (datetime('now')),
            created_by  TEXT    DEFAULT 'admin'
        );

        -- ── Attendance ────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS attendance (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id  INTEGER NOT NULL REFERENCES students(id),
            date        TEXT    NOT NULL DEFAULT (date('now')),
            status      TEXT    NOT NULL DEFAULT 'present',
            UNIQUE(student_id, date)
        );

        -- ── Indexes ───────────────────────────────────────────────
        CREATE INDEX IF NOT EXISTS idx_payments_student  ON payments(student_id);
        CREATE INDEX IF NOT EXISTS idx_payments_month    ON payments(month);
        CREATE INDEX IF NOT EXISTS idx_students_class    ON students(class);
        CREATE INDEX IF NOT EXISTS idx_attendance_date   ON attendance(date);
    """)
    conn.commit()


def row_to_dict(row: sqlite3.Row) -> dict:
    return dict(row) if row else {}


def rows_to_list(rows) -> list[dict]:
    return [dict(r) for r in rows]