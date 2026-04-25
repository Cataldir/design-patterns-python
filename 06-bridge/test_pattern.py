# test_bridge.py — Verify bridge combinations and additive growth
import pytest

from good_example import (
    Circle,
    RasterRenderer,
    Renderer,
    Shape,
    Square,
    VectorRenderer,
)


@pytest.mark.parametrize(
    ("shape_cls", "renderer", "expected_shape", "expected_style"),
    [
        (Circle, VectorRenderer(), "circle", "vectors"),
        (Circle, RasterRenderer(), "circle", "pixels"),
        (Square, VectorRenderer(), "square", "vectors"),
        (Square, RasterRenderer(), "square", "pixels"),
    ],
)
def test_bridge_combinations(
    shape_cls: type[Shape],
    renderer: Renderer,
    expected_shape: str,
    expected_style: str,
) -> None:
    result = shape_cls(renderer=renderer).draw()
    assert expected_shape in result
    assert expected_style in result


def test_additive_growth() -> None:
    """Adding a shape or renderer requires zero changes to existing code."""

    class Triangle(Shape):
        def draw(self) -> str:
            return self.renderer.render("triangle")

    class SVGRenderer:
        def render(self, shape_name: str) -> str:
            return f"Drawing {shape_name} as SVG"

    assert "triangle" in Triangle(renderer=VectorRenderer()).draw()
    assert "SVG" in Circle(renderer=SVGRenderer()).draw()
