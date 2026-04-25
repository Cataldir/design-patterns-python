# good_example.py — Bridge: Renderer Protocol + Shape with injected renderer
from dataclasses import dataclass
from typing import Protocol


class Renderer(Protocol):
    def render(self, shape_name: str) -> str: ...


class VectorRenderer:
    def render(self, shape_name: str) -> str:
        return f"Drawing {shape_name} as vectors"


class RasterRenderer:
    def render(self, shape_name: str) -> str:
        return f"Drawing {shape_name} as pixels"


@dataclass
class Shape:
    renderer: Renderer

    def draw(self) -> str:
        raise NotImplementedError


class Circle(Shape):
    def draw(self) -> str:
        return self.renderer.render("circle")


class Square(Shape):
    def draw(self) -> str:
        return self.renderer.render("square")


if __name__ == "__main__":
    for renderer in (VectorRenderer(), RasterRenderer()):
        for shape_cls in (Circle, Square):
            shape = shape_cls(renderer=renderer)
            print(shape.draw())
