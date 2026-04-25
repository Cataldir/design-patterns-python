# test_prototype.py — Verify clones are fully independent
import copy

import pytest

from good_example import GameUnit, Inventory


@pytest.fixture
def base_archer() -> GameUnit:
    return GameUnit("Archer", 100, 5, Inventory(["bow", "arrows"], {"weapon": "bow"}))


def test_deepcopy_produces_equal_but_independent_clone(base_archer: GameUnit) -> None:
    clone = copy.deepcopy(base_archer)
    assert clone.name == base_archer.name
    assert clone.inventory.items == base_archer.inventory.items
    assert clone.inventory is not base_archer.inventory


def test_modifying_clone_inventory_does_not_affect_original(base_archer: GameUnit) -> None:
    clone = copy.deepcopy(base_archer)
    clone.inventory.items.append("shield")
    clone.inventory.equipment["armor"] = "chainmail"
    assert "shield" not in base_archer.inventory.items
    assert "armor" not in base_archer.inventory.equipment
