from collections.abc import Iterator
from datetime import date
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.db import connect, get_db
from app.main import app
from app.seed import seed

END = date(2026, 10, 22)


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    """API client backed by a small, deterministic, throwaway database."""
    db_file = tmp_path / "test.db"
    conn = connect(db_file)
    seed(conn, end=END, weeks=8)
    conn.close()

    def override() -> Iterator[object]:
        c = connect(db_file)
        try:
            yield c
        finally:
            c.close()

    app.dependency_overrides[get_db] = override
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
