# bad_example.py — Manual duplication forgets to deep-copy nested state
from dataclasses import dataclass, field


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


def spawn_archer(name: str, template: GameUnit) -> GameUnit:
    """Attempt to clone a template — shares inventory by mistake."""
    return GameUnit(
        name=name,
        hit_points=template.hit_points,
        level=template.level,
        inventory=template.inventory,  # BUG: shared reference
    )


if __name__ == "__main__":
    base = GameUnit("Archer", 100, 5, Inventory(["bow", "arrows"], {"weapon": "bow"}))
    clone = spawn_archer("Archer_2", base)
    clone.inventory.items.append("poison_arrows")
    print(f"Base items:  {base.inventory.items}")
    print(f"Clone items: {clone.inventory.items}")
    # Both print: ['bow', 'arrows', 'poison_arrows'] — shared state!
