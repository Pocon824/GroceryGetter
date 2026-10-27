"""SQLite connection handling and schema."""

import os
import sqlite3
from collections.abc import Iterator
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    category TEXT
);

CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY,
    item_id INTEGER NOT NULL REFERENCES items(id),
    store TEXT NOT NULL,
    observed_on TEXT NOT NULL,           -- ISO date, YYYY-MM-DD
    price REAL NOT NULL,                 -- shelf price as shown
    unit_price REAL NOT NULL,            -- normalized: per kg, per L, or per each
    unit_basis TEXT NOT NULL CHECK (unit_basis IN ('kg', 'L', 'each')),
    price_type TEXT NOT NULL CHECK (price_type IN ('sale', 'regular')),
    source_type TEXT NOT NULL DEFAULT 'flyer'
        CHECK (source_type IN ('flyer', 'receipt', 'in_store'))
);

CREATE INDEX IF NOT EXISTS idx_obs_item_date ON observations(item_id, observed_on);
"""


def db_path() -> Path:
    return Path(os.environ.get("GROCERYGETTER_DB", ROOT / "data" / "grocery.db"))


def connect(path: Path | str | None = None) -> sqlite3.Connection:
    target = Path(path) if path else db_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    return conn


def get_db() -> Iterator[sqlite3.Connection]:
    """FastAPI dependency: one connection per request."""
    conn = connect()
    try:
        yield conn
    finally:
        conn.close()
