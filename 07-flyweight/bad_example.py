# bad_example.py - every Particle duplicates intrinsic state
import sys


class Particle:
    def __init__(
        self,
        color: str,
        texture: str,
        sprite_w: int,
        sprite_h: int,
        x: float,
        y: float,
    ) -> None:
        self.color = color
        self.texture = texture
        self.sprite_w = sprite_w
        self.sprite_h = sprite_h
        self.x = x
        self.y = y


def create_particles(n: int = 10_000) -> list[Particle]:
    return [
        Particle(
            color="orange",
            texture="assets/fire_spark.png",
            sprite_w=16,
            sprite_h=16,
            x=float(i % 800),
            y=float(i % 600),
        )
        for i in range(n)
    ]


if __name__ == "__main__":
    particles = create_particles()
    sample = particles[0]
    print(f"Instance __dict__ size : {sys.getsizeof(sample.__dict__)} bytes")
    print(f"Total instances        : {len(particles)}")
    total = sum(sys.getsizeof(p.__dict__) for p in particles)
    print(f"Sum of __dict__ sizes  : {total:,} bytes")
