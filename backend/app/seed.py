"""Generate a fake but realistic price history for development and tests.

Usage (from backend/):  python -m app.seed --reset
"""

import argparse
import random
import sqlite3
from datetime import date, timedelta

from app.db import connect

STORES = ["nofrills", "walmart", "foodbasics"]

# name, category, unit basis, typical unit price (CAD), typical pack size in that basis
CATALOG = [
    ("chicken thighs, bone-in", "meat", "kg", 9.50, 1.2),
    ("ground beef, lean", "meat", "kg", 14.00, 0.45),
    ("salmon fillets, frozen", "seafood", "kg", 22.00, 0.4),
    ("butter, salted", "dairy", "kg", 13.20, 0.454),
    ("cheddar cheese, block", "dairy", "kg", 15.00, 0.5),
    ("eggs, large", "dairy", "each", 0.40, 12),
    ("milk, 2%", "dairy", "L", 1.55, 4),
    ("bananas", "produce", "kg", 1.75, 1.0),
    ("broccoli crowns", "produce", "kg", 4.40, 0.6),
    ("pasta, dry", "pantry", "kg", 2.60, 0.9),
    ("rice, long grain", "pantry", "kg", 2.90, 2.0),
    ("canned tomatoes", "pantry", "kg", 2.40, 0.796),
]


def seed(
    conn: sqlite3.Connection,
    end: date | None = None,
    weeks: int = 26,
    random_seed: int = 42,
) -> None:
    rng = random.Random(random_seed)
    end = end or date.today()

    for name, category, basis, base, pack in CATALOG:
        conn.execute("INSERT OR IGNORE INTO items (name, category) VALUES (?, ?)", (name, category))
        item_id = conn.execute("SELECT id FROM items WHERE name = ?", (name,)).fetchone()["id"]
        store_factor = {s: rng.uniform(0.96, 1.04) for s in STORES}

        for w in range(weeks - 1, -1, -1):
            week_date = (end - timedelta(weeks=w)).isoformat()
            drift = 1 + 0.002 * (weeks - 1 - w)  # slow inflation

            for store in STORES:
                if rng.random() < 0.22:
                    unit = base * drift * store_factor[store] * (1 - rng.uniform(0.15, 0.40))
                    _insert(conn, item_id, store, week_date, unit, pack, basis, "sale", "flyer")

            if w % 4 == 0:
                store = rng.choice(STORES)
                unit = base * drift * store_factor[store] * rng.uniform(0.99, 1.03)
                _insert(conn, item_id, store, week_date, unit, pack, basis, "regular", "receipt")

    conn.commit()


def _insert(
    conn: sqlite3.Connection,
    item_id: int,
    store: str,
    observed_on: str,
    unit: float,
    pack: float,
    basis: str,
    price_type: str,
    source_type: str,
) -> None:
    price = round(unit * pack, 2)
    unit_price = round(price / pack, 4)
    conn.execute(
        """INSERT INTO observations
           (item_id, store, observed_on, price, unit_price, unit_basis, price_type, source_type)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (item_id, store, observed_on, price, unit_price, basis, price_type, source_type),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed the database with fake price history")
    parser.add_argument("--reset", action="store_true", help="delete existing data first")
    parser.add_argument("--end", type=date.fromisoformat, help="last week to generate (YYYY-MM-DD)")
    args = parser.parse_args()

    conn = connect()
    if args.reset:
        conn.execute("DELETE FROM observations")
        conn.execute("DELETE FROM items")
        conn.commit()
    elif conn.execute("SELECT COUNT(*) AS n FROM items").fetchone()["n"]:
        print("Database already has data. Use --reset to replace it.")
        return
    seed(conn, end=args.end)
    n = conn.execute("SELECT COUNT(*) AS n FROM observations").fetchone()["n"]
    print(f"Seeded {len(CATALOG)} items and {n} observations.")


if __name__ == "__main__":
    main()
