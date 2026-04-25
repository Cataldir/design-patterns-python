# good_example.py - Flyweight: shared ParticleType + slim Particle
import sys


class ParticleType:
    __slots__ = ("color", "texture", "sprite_w", "sprite_h")
    _cache: dict[tuple[str, str, int, int], "ParticleType"] = {}

    def __new__(
        cls,
        color: str,
        texture: str,
        sprite_w: int,
        sprite_h: int,
    ) -> "ParticleType":
        key = (color, texture, sprite_w, sprite_h)
        if key not in cls._cache:
            instance = super().__new__(cls)
            instance.color = color
            instance.texture = texture
            instance.sprite_w = sprite_w
            instance.sprite_h = sprite_h
            cls._cache[key] = instance
        return cls._cache[key]


class Particle:
    __slots__ = ("particle_type", "x", "y")

    def __init__(self, particle_type: ParticleType, x: float, y: float) -> None:
        self.particle_type = particle_type
        self.x = x
        self.y = y


def create_particles(n: int = 10_000) -> list[Particle]:
    shared_type = ParticleType("orange", "assets/fire_spark.png", 16, 16)
    return [
        Particle(particle_type=shared_type, x=float(i % 800), y=float(i % 600))
        for i in range(n)
    ]


if __name__ == "__main__":
    particles = create_particles()
    sample = particles[0]
    print(f"Particle  sys.getsizeof : {sys.getsizeof(sample)} bytes")
    print(f"ParticleType getsizeof  : {sys.getsizeof(sample.particle_type)} bytes")
    print(f"Unique ParticleType ids : {len({id(p.particle_type) for p in particles})}")
    total = sum(sys.getsizeof(p) for p in particles)
    print(f"Sum of Particle sizes   : {total:,} bytes")
