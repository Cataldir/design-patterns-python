# test_lab.py — Tests for Lab L2: Command + Observer Pipeline
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.modules.pop("solution", None)

import pytest

from solution import (
    ChargePayment,
    EventBus,
    OrderEvent,
    OrderPipeline,
    ShipOrder,
    ValidateOrder,
)


@pytest.fixture
def bus_and_log() -> tuple[EventBus, list[OrderEvent]]:
    log: list[OrderEvent] = []
    bus = EventBus()
    bus.subscribe(lambda e: log.append(e))
    return bus, log


def test_full_pipeline_logs_three_events(
    bus_and_log: tuple[EventBus, list[OrderEvent]],
) -> None:
    bus, log = bus_and_log
    pipeline = OrderPipeline()
    pipeline.run(ValidateOrder("ORD-001", bus))
    pipeline.run(ChargePayment("ORD-001", 50.0, bus))
    pipeline.run(ShipOrder("ORD-001", bus))
    assert len(log) == 3
    assert all(e.status == "executed" for e in log)


def test_undo_last_generates_undone_event(
    bus_and_log: tuple[EventBus, list[OrderEvent]],
) -> None:
    bus, log = bus_and_log
    pipeline = OrderPipeline()
    pipeline.run(ValidateOrder("ORD-001", bus))
    pipeline.undo_last()
    assert len(log) == 2
    assert log[-1].status == "undone"
    assert log[-1].action == "validate"


def test_undo_all_reverses_in_lifo_order(
    bus_and_log: tuple[EventBus, list[OrderEvent]],
) -> None:
    bus, log = bus_and_log
    pipeline = OrderPipeline()
    pipeline.run(ValidateOrder("ORD-001", bus))
    pipeline.run(ChargePayment("ORD-001", 50.0, bus))
    pipeline.undo_all()
    undone = [e for e in log if e.status == "undone"]
    assert len(undone) == 2
    assert undone[0].action == "charge"
    assert undone[1].action == "validate"
