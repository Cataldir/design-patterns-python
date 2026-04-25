# bad_example.py — 2 shapes x 2 renderers = 4 classes, grows as N*M


class VectorCircle:
    def draw(self) -> str:
        return "Drawing circle as vectors"


class RasterCircle:
    def draw(self) -> str:
        return "Drawing circle as pixels"


class VectorSquare:
    def draw(self) -> str:
        return "Drawing square as vectors"


class RasterSquare:
    def draw(self) -> str:
        return "Drawing square as pixels"


def render_all() -> list[str]:
    shapes = [VectorCircle(), RasterCircle(), VectorSquare(), RasterSquare()]
    return [s.draw() for s in shapes]


if __name__ == "__main__":
    for line in render_all():
        print(line)
