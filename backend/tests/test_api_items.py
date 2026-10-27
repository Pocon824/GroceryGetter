from fastapi.testclient import TestClient


def test_list_items_returns_all_with_latest_price(client: TestClient) -> None:
    response = client.get("/api/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 12
    names = [i["name"] for i in items]
    assert names == sorted(names)
    assert all(i["observation_count"] > 0 for i in items)
    assert all(i["latest_unit_price"] is not None for i in items)


def test_list_items_filters_by_name(client: TestClient) -> None:
    response = client.get("/api/items", params={"q": "CHICKEN"})
    assert [i["name"] for i in response.json()] == ["chicken thighs, bone-in"]


def test_list_items_no_match_returns_empty_list(client: TestClient) -> None:
    assert client.get("/api/items", params={"q": "zzz"}).json() == []


def test_item_detail_has_consistent_stats(client: TestClient) -> None:
    item_id = client.get("/api/items").json()[0]["id"]
    body = client.get(f"/api/items/{item_id}").json()
    stats = body["stats"]
    assert stats["observation_count"] == len(body["prices"])
    assert stats["min_unit_price"] <= stats["median_unit_price"] <= stats["max_unit_price"]
    assert stats["latest_unit_price"] == body["prices"][-1]["unit_price"]


def test_item_detail_prices_are_in_date_order(client: TestClient) -> None:
    item_id = client.get("/api/items").json()[0]["id"]
    dates = [p["observed_on"] for p in client.get(f"/api/items/{item_id}").json()["prices"]]
    assert dates == sorted(dates)


def test_item_detail_filters_by_store(client: TestClient) -> None:
    item_id = client.get("/api/items").json()[0]["id"]
    body = client.get(f"/api/items/{item_id}", params={"store": "walmart"}).json()
    assert body["prices"]
    assert {p["store"] for p in body["prices"]} == {"walmart"}


def test_item_detail_unknown_store_gives_empty_prices_and_null_stats(client: TestClient) -> None:
    item_id = client.get("/api/items").json()[0]["id"]
    body = client.get(f"/api/items/{item_id}", params={"store": "nowhere"}).json()
    assert body["prices"] == []
    assert body["stats"] is None


def test_item_detail_missing_item_is_404(client: TestClient) -> None:
    assert client.get("/api/items/99999").status_code == 404
