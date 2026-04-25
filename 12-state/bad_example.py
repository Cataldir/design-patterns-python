# bad_example.py - nested if-elif managing order states with duplicated logic
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Order:
    items: list[str] = field(default_factory=list)
    status: str = "pending"

    def process(self) -> str:
        if self.status == "pending":
            self.status = "paid"
            return f"Payment accepted for {len(self.items)} item(s)"
        elif self.status == "paid":
            self.status = "shipped"
            return f"Shipped {len(self.items)} item(s)"
        elif self.status == "shipped":
            self.status = "delivered"
            return f"Delivered {len(self.items)} item(s)"
        elif self.status == "delivered":
            raise RuntimeError("Order already delivered")
        else:
            raise ValueError(f"Unknown status: {self.status}")

    def cancel(self) -> str:
        if self.status == "pending":
            self.status = "cancelled"
            return "Order cancelled before payment"
        elif self.status == "paid":
            self.status = "cancelled"
            return "Order cancelled \u2014 refund initiated"
        elif self.status == "shipped":
            raise RuntimeError("Cannot cancel a shipped order")
        elif self.status == "delivered":
            raise RuntimeError("Cannot cancel a delivered order")
        else:
            raise ValueError(f"Unknown status: {self.status}")


if __name__ == "__main__":
    order = Order(items=["Laptop", "Mouse"])
    print(order.process())
    print(order.process())
    print(order.process())
