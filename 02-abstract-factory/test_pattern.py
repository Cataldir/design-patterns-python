# test_abstract_factory.py — Verify each factory produces a consistent family
import pytest

from good_example import (
    DarkButton, DarkCheckbox, DarkDialog, DarkThemeFactory,
    LightButton, LightCheckbox, LightDialog, LightThemeFactory,
)

FAMILIES = [
    (LightThemeFactory, LightButton, LightDialog, LightCheckbox),
    (DarkThemeFactory, DarkButton, DarkDialog, DarkCheckbox),
]


@pytest.mark.parametrize("factory_cls,btn,dlg,chk", FAMILIES)
def test_factory_produces_matching_family(
    factory_cls: type, btn: type, dlg: type, chk: type,
) -> None:
    factory = factory_cls()
    assert type(factory.create_button(label="OK")) is btn
    assert type(factory.create_dialog(title="Info")) is dlg
    assert type(factory.create_checkbox(label="Agree")) is chk


@pytest.mark.parametrize("factory_cls", [LightThemeFactory, DarkThemeFactory])
def test_all_components_render_non_empty(factory_cls: type) -> None:
    factory = factory_cls()
    for component in [
        factory.create_button(label="X"),
        factory.create_dialog(title="Y"),
        factory.create_checkbox(label="Z"),
    ]:
        assert len(component.render()) > 0
