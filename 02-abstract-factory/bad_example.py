# bad_example.py — Mixing UI components from different theme families
from dataclasses import dataclass


@dataclass
class LightButton:
    label: str

    def render(self) -> str:
        return f"[LightButton '{self.label}' | bg=white text=black]"


@dataclass
class DarkDialog:
    title: str

    def render(self) -> str:
        return f"[DarkDialog '{self.title}' | bg=black border=white]"


@dataclass
class LightCheckbox:
    label: str

    def render(self) -> str:
        return f"[LightCheckbox '{self.label}' | border=gray check=black]"


def build_form() -> list[str]:
    """Nothing prevents mixing families — visual inconsistency."""
    button = LightButton(label="Submit")
    dialog = DarkDialog(title="Confirm")
    checkbox = LightCheckbox(label="Remember me")
    return [button.render(), dialog.render(), checkbox.render()]


if __name__ == "__main__":
    for component in build_form():
        print(component)
