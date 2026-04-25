# bad_example.py - OrderService directly calling every downstream service
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EmailService:
    def send(self, order_id: str, template: str) -> str:
        return f"Email '{template}' sent for order {order_id}"


@dataclass
class InventoryService:
    def decrement(self, order_id: str) -> str:
        return f"Inventory decremented for order {order_id}"


@dataclass
class AnalyticsService:
    def track(self, order_id: str, event: str) -> str:
        return f"Tracked '{event}' for order {order_id}"


@dataclass
class OrderService:
    email: EmailService
    inventory: InventoryService
    analytics: AnalyticsService

    def complete_order(self, order_id: str) -> list[str]:
        results: list[str] = []
        results.append(f"Order {order_id} marked as completed")
        results.append(self.email.send(order_id, "order_confirmation"))
        results.append(self.inventory.decrement(order_id))
        results.append(self.analytics.track(order_id, "order_completed"))
        return results


if __name__ == "__main__":
    service = OrderService(
        email=EmailService(),
        inventory=InventoryService(),
        analytics=AnalyticsService(),
    )
    for line in service.complete_order("ORD-001"):
        print(line)
