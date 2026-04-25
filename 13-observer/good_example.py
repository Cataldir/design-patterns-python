# good_example.py - EventBus with dataclass events, weak references, and typed handlers
from __future__ import annotations

import weakref
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass(frozen=True)
class OrderPlaced:
    order_id: str
    item_count: int
    total: float


type Handler[E] = Callable[[E], None]

type _Entry = weakref.ref[Callable[..., None]] | Callable[..., None]


class EventBus:
    def __init__(self) -> None:
        self._handlers: defaultdict[type, list[_Entry]] = defaultdict(list)

    def subscribe[E](self, event_type: type[E], handler: Handler[E]) -> None:
        if hasattr(handler, "__self__"):
            ref = weakref.WeakMethod(handler)
            self._handlers[event_type].append(ref)
        else:
            self._handlers[event_type].append(handler)

    def publish[E](self, event: E) -> None:
        live: list[_Entry] = []
        for entry in self._handlers[type(event)]:
            if isinstance(entry, weakref.ref):
                callback = entry()
                if callback is not None:
                    callback(event)
                    live.append(entry)
            else:
                entry(event)
                live.append(entry)
        self._handlers[type(event)] = live


@dataclass
class EmailHandler:
    sent: list[str] = field(default_factory=list)

    def on_order_placed(self, event: OrderPlaced) -> None:
        self.sent.append(f"Confirmation for {event.order_id}")


@dataclass
class InventoryHandler:
    adjustments: list[str] = field(default_factory=list)

    def on_order_placed(self, event: OrderPlaced) -> None:
        self.adjustments.append(
            f"Reserved {event.item_count} item(s) for {event.order_id}"
        )


@dataclass
class AnalyticsHandler:
    events: list[str] = field(default_factory=list)

    def on_order_placed(self, event: OrderPlaced) -> None:
        self.events.append(f"Tracked ${event.total:.2f} sale for {event.order_id}")


def complete_order(
    bus: EventBus, order_id: str, items: list[str], total: float
) -> None:
    event = OrderPlaced(order_id=order_id, item_count=len(items), total=total)
    bus.publish(event)


if __name__ == "__main__":
    bus = EventBus()
    email = EmailHandler()
    inventory = InventoryHandler()
    analytics = AnalyticsHandler()

    bus.subscribe(OrderPlaced, email.on_order_placed)
    bus.subscribe(OrderPlaced, inventory.on_order_placed)
    bus.subscribe(OrderPlaced, analytics.on_order_placed)

    complete_order(bus, "ORD-001", ["Laptop", "Mouse"], 1299.99)
    print(email.sent)
    print(inventory.adjustments)
    print(analytics.events)
