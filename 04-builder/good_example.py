# good_example.py — Builder: fluent construction with validation
from dataclasses import dataclass


@dataclass(frozen=True)
class Pizza:
    size: str
    crust_type: str
    sauce: str
    cheese: str
    toppings: tuple[str, ...]


class PizzaBuilder:
    def __init__(self, size: str) -> None:
        self._size = size
        self._crust = "classic"
        self._sauce = "tomato"
        self._cheese = "mozzarella"
        self._toppings: list[str] = []

    def set_crust(self, crust: str) -> "PizzaBuilder":
        self._crust = crust
        return self

    def set_sauce(self, sauce: str) -> "PizzaBuilder":
        self._sauce = sauce
        return self

    def set_cheese(self, cheese: str) -> "PizzaBuilder":
        self._cheese = cheese
        return self

    def add_topping(self, topping: str) -> "PizzaBuilder":
        self._toppings.append(topping)
        return self

    def build(self) -> Pizza:
        if self._size not in ("small", "medium", "large"):
            raise ValueError(f"Invalid size: {self._size}")
        if len(self._toppings) > 10:
            raise ValueError("Maximum 10 toppings allowed")
        return Pizza(
            size=self._size, crust_type=self._crust,
            sauce=self._sauce, cheese=self._cheese,
            toppings=tuple(self._toppings),
        )


if __name__ == "__main__":
    pizza = (
        PizzaBuilder("large")
        .set_crust("thin")
        .add_topping("pepperoni")
        .add_topping("mushrooms")
        .build()
    )
    print(pizza)
