from pathlib import Path

from app.db import connect
from app.seed import CATALOG, seed
from tests.conftest import END


def _dump(path: Path) -> list[tuple[object, ...]]:
    conn = connect(path)
    rows = conn.execute(
        "SELECT item_id, store, observed_on, price, price_type FROM observations ORDER BY id"
    ).fetchall()
    conn.close()
    return [tuple(r) for r in rows]


def test_seed_is_deterministic(tmp_path: Path) -> None:
    a, b = tmp_path / "a.db", tmp_path / "b.db"
    for path in (a, b):
        conn = connect(path)
        seed(conn, end=END, weeks=6)
        conn.close()
    assert _dump(a) == _dump(b)


def test_seed_creates_every_catalog_item(tmp_path: Path) -> None:
    conn = connect(tmp_path / "c.db")
    seed(conn, end=END, weeks=6)
    count = conn.execute("SELECT COUNT(*) AS n FROM items").fetchone()["n"]
    assert count == len(CATALOG)
