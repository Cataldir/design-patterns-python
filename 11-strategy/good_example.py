# good_example.py - Strategy pattern with Protocol and class/function strategies
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class DiscountStrategy(Protocol):
    def __call__(self, subtotal: float) -> float: ...


class RegularDiscount:
    def __call__(self, subtotal: float) -> float:
        return subtotal * 0.05


class PremiumDiscount:
    def __call__(self, subtotal: float) -> float:
        return subtotal * 0.10


class VipDiscount:
    def __call__(self, subtotal: float) -> float:
        return subtotal * 0.20


class EmployeeDiscount:
    def __call__(self, subtotal: float) -> float:
        return subtotal * 0.30


class TieredDiscount:
    """Richer strategy that holds state: threshold determines rate."""

    def __init__(self, threshold: float, low_rate: float, high_rate: float) -> None:
        self._threshold = threshold
        self._low_rate = low_rate
        self._high_rate = high_rate

    def __call__(self, subtotal: float) -> float:
        rate = self._high_rate if subtotal >= self._threshold else self._low_rate
        return subtotal * rate


def seasonal_sale(subtotal: float) -> float:
    """Plain function strategy — no class needed."""
    return subtotal * 0.15


def no_discount(subtotal: float) -> float:
    return 0.0


@dataclass
class Order:
    items: list[tuple[str, float]]
    discount_strategy: DiscountStrategy

    @property
    def subtotal(self) -> float:
        return sum(price for _, price in self.items)

    def discount(self) -> float:
        return self.discount_strategy(self.subtotal)

    def final_total(self) -> float:
        return self.subtotal - self.discount()

    def summary(self) -> str:
        return (
            f"Subtotal: {self.subtotal:.2f} | "
            f"Discount: {self.discount():.2f} | "
            f"Total: {self.final_total():.2f}"
        )


if __name__ == "__main__":
    items = [("Laptop", 1200.0), ("Mouse", 60.0)]

    strategies: list[tuple[str, DiscountStrategy]] = [
        ("Regular", RegularDiscount()),
        ("Premium", PremiumDiscount()),
        ("VIP", VipDiscount()),
        ("Employee", EmployeeDiscount()),
        ("Seasonal", seasonal_sale),
        ("Tiered", TieredDiscount(threshold=500.0, low_rate=0.05, high_rate=0.12)),
        ("None", no_discount),
    ]

    for label, strategy in strategies:
        order = Order(items=items, discount_strategy=strategy)
        print(f"{label:>10}: {order.summary()}")
