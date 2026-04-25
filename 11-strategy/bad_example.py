# bad_example.py - discount logic embedded in one function with if-elif chain
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Order:
    customer_type: str
    items: list[tuple[str, float]]

    @property
    def subtotal(self) -> float:
        return sum(price for _, price in self.items)

    def final_total(self) -> float:
        discount = self._calculate_discount()
        return self.subtotal - discount

    def _calculate_discount(self) -> float:
        if self.customer_type == "regular":
            return self.subtotal * 0.05
        elif self.customer_type == "premium":
            return self.subtotal * 0.10
        elif self.customer_type == "vip":
            return self.subtotal * 0.20
        elif self.customer_type == "employee":
            return self.subtotal * 0.30
        else:
            raise ValueError(f"Unknown customer type: {self.customer_type}")

    def summary(self) -> str:
        return (
            f"Customer: {self.customer_type} | "
            f"Subtotal: {self.subtotal:.2f} | "
            f"Total: {self.final_total():.2f}"
        )


if __name__ == "__main__":
    orders = [
        Order("regular", [("Book", 50.0), ("Pen", 10.0)]),
        Order("premium", [("Laptop", 1200.0)]),
        Order("vip", [("Phone", 800.0), ("Case", 40.0)]),
        Order("employee", [("Monitor", 400.0)]),
    ]
    for order in orders:
        print(order.summary())
