# test_state.py - pytest verifying behavior changes at each transition step
from __future__ import annotations

import pytest

from good_example import (
    DeliveredState,
    OrderContext,
    OrderStatus,
    PaidState,
    PendingState,
    ShippedState,
)


class TestStateTransitions:
    def test_pending_to_paid(self) -> None:
        order = OrderContext(items=["Book"])
        assert order.status is OrderStatus.PENDING
        result = order.process()
        assert order.status is OrderStatus.PAID
        assert "Payment accepted" in result

    def test_paid_to_shipped(self) -> None:
        order = OrderContext(items=["Book"], state=PaidState())
        result = order.process()
        assert order.status is OrderStatus.SHIPPED
        assert "Shipped" in result

    def test_shipped_to_delivered(self) -> None:
        order = OrderContext(items=["Book"], state=ShippedState())
        result = order.process()
        assert order.status is OrderStatus.DELIVERED
        assert "Delivered" in result

    def test_delivered_raises_runtime_error(self) -> None:
        order = OrderContext(items=["Book"], state=DeliveredState())
        with pytest.raises(RuntimeError, match="already delivered"):
            order.process()


class TestFullLifecycle:
    def test_complete_order_flow(self) -> None:
        order = OrderContext(items=["Laptop", "Mouse"])
        expected: list[tuple[OrderStatus, str]] = [
            (OrderStatus.PAID, "Payment accepted"),
            (OrderStatus.SHIPPED, "Shipped"),
            (OrderStatus.DELIVERED, "Delivered"),
        ]
        for status, fragment in expected:
            result = order.process()
            assert order.status is status
            assert fragment in result

    def test_next_state_returns_correct_successor(self) -> None:
        assert isinstance(PendingState().next_state(), PaidState)
        assert isinstance(PaidState().next_state(), ShippedState)
        assert isinstance(ShippedState().next_state(), DeliveredState)
        assert isinstance(DeliveredState().next_state(), DeliveredState)

    def test_status_property_matches_enum(self) -> None:
        assert PendingState().status is OrderStatus.PENDING
        assert PaidState().status is OrderStatus.PAID
        assert ShippedState().status is OrderStatus.SHIPPED
        assert DeliveredState().status is OrderStatus.DELIVERED
