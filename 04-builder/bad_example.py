# bad_example.py — Telescoping constructor with too many parameters
from dataclasses import dataclass


@dataclass
class Pizza:
    size: str
    crust_type: str
    sauce: str | None = None
    cheese: str | None = None
    topping_1: str | None = None
    topping_2: str | None = None
    topping_3: str | None = None
    topping_4: str | None = None
    topping_5: str | None = None
    topping_6: str | None = None
    is_vegan: bool = False


if __name__ == "__main__":
    pepperoni = Pizza(
        "large", "classic", "tomato", "mozzarella",
        "pepperoni", "mushrooms", None, None, None, None, False,
    )
    print(pepperoni)
