# good_example.py - State pattern with Protocol, enum identifiers, and dataclass context
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Protocol


class OrderStatus(Enum):
    PENDING = auto()
    PAID = auto()
    SHIPPED = auto()
    DELIVERED = auto()


class OrderState(Protocol):
    @property
    def status(self) -> OrderStatus: ...
    def handle(self, context: OrderContext) -> str: ...
    def next_state(self) -> OrderState: ...


class PendingState:
    @property
    def status(self) -> OrderStatus:
        return OrderStatus.PENDING

    def handle(self, context: OrderContext) -> str:
        message = f"Payment accepted for {len(context.items)} item(s)"
        context.state = self.next_state()
        return message

    def next_state(self) -> OrderState:
        return PaidState()


class PaidState:
    @property
    def status(self) -> OrderStatus:
        return OrderStatus.PAID

    def handle(self, context: OrderContext) -> str:
        message = f"Shipped {len(context.items)} item(s)"
        context.state = self.next_state()
        return message

    def next_state(self) -> OrderState:
        return ShippedState()


class ShippedState:
    @property
    def status(self) -> OrderStatus:
        return OrderStatus.SHIPPED

    def handle(self, context: OrderContext) -> str:
        message = f"Delivered {len(context.items)} item(s)"
        context.state = self.next_state()
        return message

    def next_state(self) -> OrderState:
        return DeliveredState()


class DeliveredState:
    @property
    def status(self) -> OrderStatus:
        return OrderStatus.DELIVERED

    def handle(self, context: OrderContext) -> str:
        raise RuntimeError("Order already delivered")

    def next_state(self) -> OrderState:
        return self


@dataclass
class OrderContext:
    items: list[str] = field(default_factory=list)
    state: OrderState = field(default_factory=PendingState)

    @property
    def status(self) -> OrderStatus:
        return self.state.status

    def process(self) -> str:
        return self.state.handle(self)


if __name__ == "__main__":
    order = OrderContext(items=["Laptop", "Mouse"])
    print(f"{order.status.name}: {order.process()}")
    print(f"{order.status.name}: {order.process()}")
    print(f"{order.status.name}: {order.process()}")
