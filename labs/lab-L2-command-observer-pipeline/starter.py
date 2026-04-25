# starter.py — Order pipeline skeleton (fill in the commands)
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


# TODO: Implement ValidateOrder, ChargePayment, ShipOrder commands
# Each command should:
# 1. Track its own state (_validated, _charged, _shipped)
# 2. Publish an OrderEvent on execute() and undo()


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
