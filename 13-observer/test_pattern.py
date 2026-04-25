# test_observer.py - pytest verifying notification delivery, ordering, and weak reference cleanup
from __future__ import annotations

import gc

import pytest

from good_example import (
    AnalyticsHandler,
    EmailHandler,
    EventBus,
    InventoryHandler,
    OrderPlaced,
)


@pytest.fixture
def bus() -> EventBus:
    return EventBus()


@pytest.fixture
def event() -> OrderPlaced:
    return OrderPlaced(order_id="ORD-001", item_count=2, total=149.99)


class TestNotificationDelivery:
    def test_single_handler_receives_event(
        self, bus: EventBus, event: OrderPlaced
    ) -> None:
        email = EmailHandler()
        bus.subscribe(OrderPlaced, email.on_order_placed)
        bus.publish(event)
        assert len(email.sent) == 1
        assert "ORD-001" in email.sent[0]

    def test_multiple_handlers_all_notified(
        self, bus: EventBus, event: OrderPlaced
    ) -> None:
        email = EmailHandler()
        inventory = InventoryHandler()
        analytics = AnalyticsHandler()
        bus.subscribe(OrderPlaced, email.on_order_placed)
        bus.subscribe(OrderPlaced, inventory.on_order_placed)
        bus.subscribe(OrderPlaced, analytics.on_order_placed)
        bus.publish(event)
        assert len(email.sent) == 1
        assert len(inventory.adjustments) == 1
        assert len(analytics.events) == 1

    def test_handler_ordering_matches_subscription(
        self, bus: EventBus, event: OrderPlaced
    ) -> None:
        call_order: list[str] = []

        def first_handler(e: OrderPlaced) -> None:
            call_order.append("first")

        def second_handler(e: OrderPlaced) -> None:
            call_order.append("second")

        bus.subscribe(OrderPlaced, first_handler)
        bus.subscribe(OrderPlaced, second_handler)
        bus.publish(event)
        assert call_order == ["first", "second"]


class TestWeakReferenceCleanup:
    def test_dead_handler_removed_after_publish(
        self, bus: EventBus, event: OrderPlaced
    ) -> None:
        email = EmailHandler()
        bus.subscribe(OrderPlaced, email.on_order_placed)
        del email
        gc.collect()
        bus.publish(event)
        assert len(bus._handlers[OrderPlaced]) == 0

    def test_live_handler_survives_cleanup(
        self, bus: EventBus, event: OrderPlaced
    ) -> None:
        email = EmailHandler()
        bus.subscribe(OrderPlaced, email.on_order_placed)
        bus.publish(event)
        assert len(bus._handlers[OrderPlaced]) == 1
        assert len(email.sent) == 1
