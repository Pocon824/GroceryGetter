# Task 2: Unit conversion (test-first)

## Why

A flyer says `$4.99/lb`, another says `$10.98/kg`, a third says `2 for $5`. To compare them
(and to decide whether a sale is a good price) every price has to become one comparable
number: dollars per kg, per litre, or per item.

## The function

```python
unit_price(price, price_is_per, pack_size=None, pack_unit=None, multi_buy_qty=None)
    -> (unit_price: float | None, basis: "kg" | "L" | "each" | None)
```

- `price`: the number printed on the flyer.
- `price_is_per`: what that price is *per*: `"lb"`, `"kg"`, `"100g"`, `"100ml"`, `"each"`, or `None`.
- `pack_size` / `pack_unit`: the size of the package, e.g. `500, "g"` or `12, "each"`.
- `multi_buy_qty`: for deals like "2 for $5", `price` is the total and this is `2`.

Results are rounded to **4 decimal places**.

## Rules

1. If `multi_buy_qty` is greater than 1, divide `price` by it first.
2. If `price_is_per` is a weight (`kg`, `g`, `100g`, `lb`, `oz`), convert to **$/kg**.
3. If `price_is_per` is a volume (`l`, `ml`, `100ml`), convert to **$/L**.
4. Otherwise, if `pack_size` is positive and `pack_unit` is known, divide by the pack's size
   in kg, L, or items.
5. Otherwise, if `price_is_per` is `"each"`, the price is already per item: **$/each**.
6. Otherwise the size can't be determined: return `(None, None)`.
7. Unit names are case-insensitive and accept common spellings: `lbs`, `litre`, `liter`, `ea`.
8. A `pack_size` of zero or less is treated as missing.

Constants: 1 lb = 0.45359237 kg, 1 oz = 0.0283495 kg.

## Examples (all verified)

| price | per | pack | multi-buy | expected |
|---|---|---|---|---|
| 4.99 | lb | | | 11.0011 per kg |
| 10.98 | kg | | | 10.98 per kg |
| 6.5 | LBS | | | 14.33 per kg |
| 2.99 | 100g | | | 29.9 per kg |
| 5.99 | each | 500 g | | 11.98 per kg |
| 1.99 | 100ml | | | 19.9 per L |
| 4.99 | each | 2 L | | 2.495 per L |
| 2.5 | each | 750 ml | | 3.3333 per L |
| 3.49 | each | 12 each | | 0.2908 per each |
| 5 | each | | 2 | 2.5 per each |
| 8 | each | 500 g | 2 | 8.0 per kg |
| 3.99 | each | 0 g | | 3.99 per each (zero pack ignored) |
| 3.99 | none | | | (None, None) |

## Your steps

1. `git checkout -b feat/unit-conversion`
2. Write the tests in `backend/tests/test_units.py` first. Group related cases with
   `@pytest.mark.parametrize`. Add a few of your own edge cases (negative price? unknown unit?).
3. Run `pytest` and confirm they **fail** (the function raises `NotImplementedError`).
4. Implement `unit_price` in `backend/app/units.py` (or send me your tests and I'll implement it).
5. Push the branch, open a pull request, and wait for CI to go green before merging.

Heads up: comparing floats with `==` is fragile. Use `pytest.approx` (the example test shows how).
