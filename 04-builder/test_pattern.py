# test_builder.py — Verify builder produces correct Pizza instances
import pytest

from good_example import Pizza, PizzaBuilder


@pytest.fixture
def builder() -> PizzaBuilder:
    return PizzaBuilder("large")


def test_builder_produces_correct_pizza(builder: PizzaBuilder) -> None:
    pizza = builder.set_crust("thin").add_topping("pepperoni").add_topping("mushrooms").build()
    assert pizza.size == "large"
    assert pizza.crust_type == "thin"
    assert pizza.toppings == ("pepperoni", "mushrooms")


def test_invalid_size_raises_error() -> None:
    with pytest.raises(ValueError, match="Invalid size"):
        PizzaBuilder("extra_extra_large").build()


def test_too_many_toppings_raises_error(builder: PizzaBuilder) -> None:
    for i in range(11):
        builder.add_topping(f"topping_{i}")
    with pytest.raises(ValueError, match="Maximum 10 toppings"):
        builder.build()
