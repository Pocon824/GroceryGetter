import sqlite3
import statistics
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from app.db import get_db
from app.schemas import ItemDetail, ItemSummary, PricePoint, PriceStats

router = APIRouter(prefix="/api/items", tags=["items"])

Db = Annotated[sqlite3.Connection, Depends(get_db)]

LIST_SQL = """
WITH ranked AS (
    SELECT item_id, store, observed_on, price, unit_price, unit_basis,
           ROW_NUMBER() OVER (PARTITION BY item_id ORDER BY observed_on DESC, id DESC) AS rn,
           COUNT(*) OVER (PARTITION BY item_id) AS n
    FROM observations
)
SELECT i.id, i.name, i.category,
       COALESCE(r.n, 0) AS observation_count,
       r.store AS latest_store, r.observed_on AS latest_observed_on,
       r.price AS latest_price, r.unit_price AS latest_unit_price, r.unit_basis
FROM items i
LEFT JOIN ranked r ON r.item_id = i.id AND r.rn = 1
WHERE (? IS NULL OR i.name LIKE '%' || ? || '%')
ORDER BY i.name
"""


@router.get("", response_model=list[ItemSummary])
def list_items(
    conn: Db,
    q: Annotated[str | None, Query(description="Filter by name (substring)")] = None,
) -> list[ItemSummary]:
    rows = conn.execute(LIST_SQL, (q, q)).fetchall()
    return [ItemSummary(**dict(row)) for row in rows]


@router.get("/{item_id}", response_model=ItemDetail)
def get_item(
    item_id: int,
    conn: Db,
    store: Annotated[str | None, Query(description="Only prices from this store")] = None,
) -> ItemDetail:
    item = conn.execute("SELECT id, name, category FROM items WHERE id = ?", (item_id,)).fetchone()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    rows = conn.execute(
        """
        SELECT observed_on, store, price, unit_price, unit_basis, price_type, source_type
        FROM observations
        WHERE item_id = ? AND (? IS NULL OR store = ?)
        ORDER BY observed_on, id
        """,
        (item_id, store, store),
    ).fetchall()
    prices = [PricePoint(**dict(row)) for row in rows]

    stats = None
    if prices:
        values = [p.unit_price for p in prices]
        stats = PriceStats(
            unit_basis=prices[-1].unit_basis,
            observation_count=len(prices),
            min_unit_price=min(values),
            median_unit_price=round(statistics.median(values), 4),
            max_unit_price=max(values),
            latest_unit_price=prices[-1].unit_price,
        )

    return ItemDetail(
        id=item["id"], name=item["name"], category=item["category"], stats=stats, prices=prices
    )
