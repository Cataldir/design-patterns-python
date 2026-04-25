# test_lab.py — Tests for Lab L1: Strategy Refactor
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.modules.pop("solution", None)

import pytest

from solution import calculate_discount


@pytest.mark.parametrize(
    ("customer_type", "total", "expected"),
    [
        ("regular", 100.0, 5.0),
        ("premium", 100.0, 10.0),
        ("vip", 100.0, 20.0),
        ("employee", 100.0, 30.0),
        ("wholesale", 5_000.0, 750.0),
        ("wholesale", 15_000.0, 3_750.0),
        ("unknown", 100.0, 0.0),
    ],
)
def test_discount(customer_type: str, total: float, expected: float) -> None:
    assert calculate_discount(total, customer_type) == pytest.approx(expected)
