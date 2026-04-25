# starter.py — Discount calculator with if-else chain (the smell)

def calculate_discount(order_total: float, customer_type: str) -> float:
    """Calculate discount — this is the code smell to refactor."""
    if customer_type == "regular":
        return order_total * 0.05
    elif customer_type == "premium":
        return order_total * 0.10
    elif customer_type == "vip":
        return order_total * 0.20
    elif customer_type == "employee":
        return order_total * 0.30
    elif customer_type == "wholesale":
        if order_total > 10_000:
            return order_total * 0.25
        return order_total * 0.15
    else:
        return 0.0


if __name__ == "__main__":
    print(calculate_discount(100.0, "regular"))
    print(calculate_discount(100.0, "vip"))
    print(calculate_discount(15_000.0, "wholesale"))
