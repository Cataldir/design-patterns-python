# good_example.py — Abstract Factory: Protocol-based theme families
from dataclasses import dataclass
from typing import Protocol


class Button(Protocol):
    def render(self) -> str: ...

class Dialog(Protocol):
    def render(self) -> str: ...

class Checkbox(Protocol):
    def render(self) -> str: ...


class ThemeFactory(Protocol):
    def create_button(self, label: str) -> Button: ...
    def create_dialog(self, title: str) -> Dialog: ...
    def create_checkbox(self, label: str) -> Checkbox: ...


# ── Light family ─────────────────────────────────────

@dataclass
class LightButton:
    label: str
    def render(self) -> str:
        return f"[LightButton '{self.label}' | bg=white text=black]"

@dataclass
class LightDialog:
    title: str
    def render(self) -> str:
        return f"[LightDialog '{self.title}' | bg=white border=gray]"

@dataclass
class LightCheckbox:
    label: str
    def render(self) -> str:
        return f"[LightCheckbox '{self.label}' | border=gray check=black]"


class LightThemeFactory:
    def create_button(self, label: str) -> Button:
        return LightButton(label=label)
    def create_dialog(self, title: str) -> Dialog:
        return LightDialog(title=title)
    def create_checkbox(self, label: str) -> Checkbox:
        return LightCheckbox(label=label)


# ── Dark family ──────────────────────────────────────

@dataclass
class DarkButton:
    label: str
    def render(self) -> str:
        return f"[DarkButton '{self.label}' | bg=black text=white]"

@dataclass
class DarkDialog:
    title: str
    def render(self) -> str:
        return f"[DarkDialog '{self.title}' | bg=black border=white]"

@dataclass
class DarkCheckbox:
    label: str
    def render(self) -> str:
        return f"[DarkCheckbox '{self.label}' | border=white check=white]"


class DarkThemeFactory:
    def create_button(self, label: str) -> Button:
        return DarkButton(label=label)
    def create_dialog(self, title: str) -> Dialog:
        return DarkDialog(title=title)
    def create_checkbox(self, label: str) -> Checkbox:
        return DarkCheckbox(label=label)


# ── Application code ─────────────────────────────────

def build_form(factory: ThemeFactory) -> list[str]:
    button = factory.create_button(label="Submit")
    dialog = factory.create_dialog(title="Confirm")
    checkbox = factory.create_checkbox(label="Remember me")
    return [button.render(), dialog.render(), checkbox.render()]


if __name__ == "__main__":
    for name, factory in [("Light", LightThemeFactory()), ("Dark", DarkThemeFactory())]:
        print(f"\n{name} theme:")
        for line in build_form(factory):
            print(f"  {line}")
