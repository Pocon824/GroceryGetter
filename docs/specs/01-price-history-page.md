# Task 1: Price history page (Angular)

## Goal

A page where you pick a grocery item and see its price history: where it's been cheapest,
what the typical price is, and what the latest price was.

## Running the backend

From `backend/` in a terminal:

```
py -3 -m venv .venv
.venv\Scripts\activate.bat
pip install -e ".[dev]"
python -m app.seed --reset
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to try every endpoint in the browser. CORS already allows
the Angular dev server at http://localhost:4200.

## The API

### `GET /api/items?q=chicken`

```json
[
  {
    "id": 1,
    "name": "chicken thighs, bone-in",
    "category": "meat",
    "observation_count": 31,
    "latest_store": "walmart",
    "latest_observed_on": "2026-10-22",
    "latest_price": 11.8,
    "latest_unit_price": 9.83,
    "unit_basis": "kg"
  }
]
```

`q` is optional. Most fields can be `null` for an item with no prices yet.

### `GET /api/items/{id}?store=walmart`

```json
{
  "id": 1,
  "name": "chicken thighs, bone-in",
  "category": "meat",
  "stats": {
    "unit_basis": "kg",
    "observation_count": 31,
    "min_unit_price": 6.1,
    "median_unit_price": 9.4,
    "max_unit_price": 10.2,
    "latest_unit_price": 9.83
  },
  "prices": [
    {
      "observed_on": "2026-04-30",
      "store": "nofrills",
      "price": 8.1,
      "unit_price": 6.75,
      "unit_basis": "kg",
      "price_type": "sale",
      "source_type": "flyer"
    }
  ]
}
```

`store` is optional (`nofrills`, `walmart`, `foodbasics`). `stats` is `null` when there are no
prices. An unknown id returns 404. Prices come back oldest first.

## What to build

1. **Items list** at `/items`: a search box and a list of items. Each row shows the name, latest
   unit price with its basis (for example `$9.83 / kg`), the store, and the date.
   Searching calls the API with `q`.
2. **Item detail** at `/items/:id`: the name, the stats (min / median / max / latest), a store
   filter, and a table of price points. Sale rows should look different from regular rows.
3. **Navigation** between the two, with a back link.
4. **States:** loading, error (API down), and empty (no matches, no prices) each show a clear message.

## Acceptance criteria

- [ ] Typing in the search box filters the list without a full page reload
- [ ] Clicking an item opens its detail page; the URL can be refreshed or shared
- [ ] The store filter changes the table and the stats together
- [ ] Prices display as dollars with two decimals; unit prices show their basis
- [ ] Loading, error, and empty states all exist and are readable
- [ ] The page works with the keyboard only (tab order, visible focus, labelled inputs)
- [ ] No `any` types in the TypeScript

## Tests you write

- A service test: `HttpTestingController` verifies the right URL and query params are called
- A component test for the list: shows rows from a mocked service; shows the empty state
- A component test for the detail: shows stats; sale rows get their distinguishing class
- Later: a Playwright test for search then open item

## Concepts to look up (angular.dev)

Components and templates, signals (`signal`, `computed`), `inject()` and services, `HttpClient`,
routing with route params, `@if` / `@for` control flow, and TypeScript interfaces.

## Tips

- Write the TypeScript interfaces by hand from the JSON above. They'll be replaced by a
  generated API client later, and having written them yourself will help you read it.
- Start with just the list, hard-coded, then wire it to the API.
- Put the API base URL in one place, not in every call.

## Stretch

- Sort the table by date or price
- A line chart of unit price over time, with sale points highlighted
- Highlight the cheapest-ever price
