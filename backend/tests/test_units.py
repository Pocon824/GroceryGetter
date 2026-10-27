"""Tests for app.units.unit_price. YOUR TASK: write these before implementing.

Workflow:
  1. git checkout -b feat/unit-conversion
  2. Turn the cases in docs/specs/02-unit-conversion.md into tests here
     (pytest.mark.parametrize keeps a table of cases short and readable).
  3. Run `pytest` and watch them fail (red).
  4. Implement unit_price in app/units.py until they pass (green).
  5. Open a pull request and wait for CI.
"""

import pytest

from app.units import unit_price


@pytest.mark.skip(reason="Example only. Delete this line when you start the task.")
def test_price_per_lb_is_converted_to_per_kg() -> None:
    value, basis = unit_price(4.99, "lb")
    assert basis == "kg"
    assert value == pytest.approx(11.0011, abs=1e-4)
