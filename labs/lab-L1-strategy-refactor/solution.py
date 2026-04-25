# solution.py — Strategy pattern with function strategies and registry
from collections.abc import Callable

type DiscountStrategy = Callable[[float], float]


def regular_discount(total: float) -> float:
    return total * 0.05


def premium_discount(total: float) -> float:
    return total * 0.10


def vip_discount(total: float) -> float:
    return total * 0.20


def employee_discount(total: float) -> float:
    return total * 0.30


def wholesale_discount(total: float) -> float:
    return total * 0.25 if total > 10_000 else total * 0.15


_STRATEGIES: dict[str, DiscountStrategy] = {
    "regular": regular_discount,
    "premium": premium_discount,
    "vip": vip_discount,
    "employee": employee_discount,
    "wholesale": wholesale_discount,
}


def calculate_discount(order_total: float, customer_type: str) -> float:
    strategy = _STRATEGIES.get(customer_type)
    if strategy is None:
        return 0.0
    return strategy(order_total)


if __name__ == "__main__":
    print(calculate_discount(100.0, "regular"))
    print(calculate_discount(100.0, "vip"))
    print(calculate_discount(15_000.0, "wholesale"))
