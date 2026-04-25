# good_example.py — Prototype: GameUnit with proper clone support
import copy
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Inventory:
    items: list[str] = field(default_factory=list)
    equipment: dict[str, str] = field(default_factory=dict)


@dataclass
class GameUnit:
    name: str
    hit_points: int
    level: int
    inventory: Inventory

    def __copy__(self) -> "GameUnit":
        return GameUnit(
            name=self.name,
            hit_points=self.hit_points,
            level=self.level,
            inventory=self.inventory,  # shallow: shares inventory
        )

    def __deepcopy__(self, memo: dict[int, Any]) -> "GameUnit":
        return GameUnit(
            name=self.name,
            hit_points=self.hit_points,
            level=self.level,
            inventory=copy.deepcopy(self.inventory, memo),
        )


if __name__ == "__main__":
    base = GameUnit("Archer", 100, 5, Inventory(["bow", "arrows"], {"weapon": "bow"}))
    clone = copy.deepcopy(base)
    clone.name = "Archer_2"
    clone.inventory.items.append("poison_arrows")
    print(f"Base items:  {base.inventory.items}")
    print(f"Clone items: {clone.inventory.items}")
    # Base: ['bow', 'arrows']  —  Clone: ['bow', 'arrows', 'poison_arrows']
