# test_strategy.py - pytest suite with parametrize over strategy variants
from __future__ import annotations

import pytest

from good_example import (
    DiscountStrategy,
    EmployeeDiscount,
    Order,
    PremiumDiscount,
    RegularDiscount,
    TieredDiscount,
    VipDiscount,
    no_discount,
    seasonal_sale,
)


class TestIndividualStrategies:
    def test_regular_discount(self) -> None:
        strategy = RegularDiscount()
        assert strategy(100.0) == pytest.approx(5.0)

    def test_premium_discount(self) -> None:
        strategy = PremiumDiscount()
        assert strategy(100.0) == pytest.approx(10.0)

    def test_vip_discount(self) -> None:
        strategy = VipDiscount()
        assert strategy(200.0) == pytest.approx(40.0)

    def test_employee_discount(self) -> None:
        strategy = EmployeeDiscount()
        assert strategy(200.0) == pytest.approx(60.0)

    def test_seasonal_sale_function(self) -> None:
        assert seasonal_sale(100.0) == pytest.approx(15.0)

    def test_no_discount_returns_zero(self) -> None:
        assert no_discount(100.0) == pytest.approx(0.0)


class TestTieredDiscount:
    def test_below_threshold_uses_low_rate(self) -> None:
        strategy = TieredDiscount(threshold=500.0, low_rate=0.05, high_rate=0.12)
        assert strategy(300.0) == pytest.approx(15.0)

    def test_at_threshold_uses_high_rate(self) -> None:
        strategy = TieredDiscount(threshold=500.0, low_rate=0.05, high_rate=0.12)
        assert strategy(500.0) == pytest.approx(60.0)

    def test_above_threshold_uses_high_rate(self) -> None:
        strategy = TieredDiscount(threshold=500.0, low_rate=0.05, high_rate=0.12)
        assert strategy(1000.0) == pytest.approx(120.0)


STRATEGY_CASES: list[tuple[str, DiscountStrategy, float, float]] = [
    ("regular", RegularDiscount(), 200.0, 190.0),
    ("premium", PremiumDiscount(), 200.0, 180.0),
    ("vip", VipDiscount(), 200.0, 160.0),
    ("employee", EmployeeDiscount(), 200.0, 140.0),
    ("seasonal", seasonal_sale, 200.0, 170.0),
    ("no_discount", no_discount, 200.0, 200.0),
    ("tiered_low", TieredDiscount(500.0, 0.05, 0.12), 200.0, 190.0),
    ("tiered_high", TieredDiscount(500.0, 0.05, 0.12), 600.0, 528.0),
]


class TestOrderWithParametrize:
    @pytest.mark.parametrize(
        ("label", "strategy", "subtotal", "expected_total"),
        STRATEGY_CASES,
        ids=[c[0] for c in STRATEGY_CASES],
    )
    def test_final_total(
        self,
        label: str,
        strategy: DiscountStrategy,
        subtotal: float,
        expected_total: float,
    ) -> None:
        order = Order(
            items=[("Item", subtotal)],
            discount_strategy=strategy,
        )
        assert order.final_total() == pytest.approx(expected_total)
