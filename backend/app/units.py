"""Unit normalization: turn a shelf price into a comparable unit price.

This is YOUR first backend task (see docs/specs/02-unit-conversion.md).
Write the tests first in tests/test_units.py, then implement.
"""


def unit_price(
    price: float,
    price_is_per: str | None,
    pack_size: float | None = None,
    pack_unit: str | None = None,
    multi_buy_qty: int | None = None,
) -> tuple[float | None, str | None]:
    """Return (unit_price, basis) where basis is 'kg', 'L' or 'each'.

    Return (None, None) when the size can't be determined.
    See the spec for the exact rules and examples.
    """
    raise NotImplementedError
