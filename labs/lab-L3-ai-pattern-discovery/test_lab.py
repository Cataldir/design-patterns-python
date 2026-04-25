# test_lab.py — Tests for Lab L3: AI-Assisted Pattern Discovery
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.modules.pop("solution", None)

from datetime import datetime, timedelta

import pytest

from solution import (
    ItemNotDamaged,
    ReturnRequest,
    WithinReturnWindow,
    validate_return,
)


@pytest.fixture
def rules() -> list:
    return [WithinReturnWindow(), ItemNotDamaged()]


def test_eligible_return(rules: list) -> None:
    request = ReturnRequest(
        order_date=datetime.now() - timedelta(days=10),
        request_date=datetime.now(),
        item_condition="new",
        reason="Changed my mind",
    )
    eligible, reasons = validate_return(request, rules)
    assert eligible is True
    assert reasons == []


def test_expired_return(rules: list) -> None:
    request = ReturnRequest(
        order_date=datetime.now() - timedelta(days=45),
        request_date=datetime.now(),
        item_condition="new",
        reason="Changed my mind",
    )
    eligible, reasons = validate_return(request, rules)
    assert eligible is False
    assert "30 days" in reasons[0]


def test_damaged_item(rules: list) -> None:
    request = ReturnRequest(
        order_date=datetime.now() - timedelta(days=5),
        request_date=datetime.now(),
        item_condition="damaged",
        reason="Broken on arrival",
    )
    eligible, reasons = validate_return(request, rules)
    assert eligible is False
    assert "Damaged" in reasons[0]


def test_both_rules_fail(rules: list) -> None:
    request = ReturnRequest(
        order_date=datetime.now() - timedelta(days=45),
        request_date=datetime.now(),
        item_condition="damaged",
        reason="Too late and broken",
    )
    eligible, reasons = validate_return(request, rules)
    assert eligible is False
    assert len(reasons) == 2
