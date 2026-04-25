# solution.py — Command + Observer order pipeline
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class OrderEvent:
    order_id: str
    action: str
    status: str  # "executed" or "undone"


class EventBus:
    def __init__(self) -> None:
        self._listeners: list[Callable[[OrderEvent], None]] = []

    def subscribe(self, listener: Callable[[OrderEvent], None]) -> None:
        self._listeners.append(listener)

    def publish(self, event: OrderEvent) -> None:
        for listener in self._listeners:
            listener(event)


class OrderCommand(Protocol):
    def execute(self) -> None: ...
    def undo(self) -> None: ...


class ValidateOrder:
    def __init__(self, order_id: str, bus: EventBus) -> None:
        self._order_id = order_id
        self._bus = bus
        self._validated = False

    def execute(self) -> None:
        self._validated = True
        self._bus.publish(OrderEvent(self._order_id, "validate", "executed"))

    def undo(self) -> None:
        self._validated = False
        self._bus.publish(OrderEvent(self._order_id, "validate", "undone"))


class ChargePayment:
    def __init__(self, order_id: str, amount: float, bus: EventBus) -> None:
        self._order_id = order_id
        self._amount = amount
        self._bus = bus
        self._charged = False

    def execute(self) -> None:
        self._charged = True
        self._bus.publish(OrderEvent(self._order_id, "charge", "executed"))

    def undo(self) -> None:
        self._charged = False
        self._bus.publish(OrderEvent(self._order_id, "charge", "undone"))


class ShipOrder:
    def __init__(self, order_id: str, bus: EventBus) -> None:
        self._order_id = order_id
        self._bus = bus
        self._shipped = False

    def execute(self) -> None:
        self._shipped = True
        self._bus.publish(OrderEvent(self._order_id, "ship", "executed"))

    def undo(self) -> None:
        self._shipped = False
        self._bus.publish(OrderEvent(self._order_id, "ship", "undone"))


class OrderPipeline:
    def __init__(self) -> None:
        self._history: list[OrderCommand] = []

    def run(self, cmd: OrderCommand) -> None:
        cmd.execute()
        self._history.append(cmd)

    def undo_last(self) -> None:
        if self._history:
            self._history.pop().undo()

    def undo_all(self) -> None:
        while self._history:
            self.undo_last()


if __name__ == "__main__":
    log: list[OrderEvent] = []
    bus = EventBus()
    bus.subscribe(lambda e: log.append(e))

    pipeline = OrderPipeline()
    pipeline.run(ValidateOrder("ORD-001", bus))
    pipeline.run(ChargePayment("ORD-001", 99.99, bus))
    pipeline.run(ShipOrder("ORD-001", bus))

    pipeline.undo_last()

    for event in log:
        print(f"{event.action:>10} → {event.status}")
