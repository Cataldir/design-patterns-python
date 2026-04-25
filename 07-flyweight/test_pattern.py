# test_flyweight.py - verify shared identity and memory savings
import sys

import pytest

from good_example import Particle, ParticleType


class TestParticleTypeCaching:
    def test_same_args_return_same_object(self) -> None:
        a = ParticleType("orange", "assets/fire_spark.png", 16, 16)
        b = ParticleType("orange", "assets/fire_spark.png", 16, 16)
        assert a is b

    def test_different_args_return_different_objects(self) -> None:
        fire = ParticleType("orange", "assets/fire_spark.png", 16, 16)
        ice = ParticleType("blue", "assets/ice_shard.png", 8, 8)
        assert fire is not ice

    def test_cache_length_matches_unique_types(self) -> None:
        ParticleType._cache.clear()
        ParticleType("red", "assets/blood.png", 4, 4)
        ParticleType("red", "assets/blood.png", 4, 4)
        ParticleType("green", "assets/leaf.png", 12, 12)
        assert len(ParticleType._cache) == 2


class TestMemorySavings:
    def test_flyweight_particles_use_less_memory(self) -> None:
        from bad_example import Particle as FatParticle
        from bad_example import create_particles as create_fat

        fat_particles = create_fat(1_000)
        fat_total = sum(sys.getsizeof(p.__dict__) for p in fat_particles)

        from good_example import create_particles as create_slim

        slim_particles = create_slim(1_000)
        slim_total = sum(sys.getsizeof(p) for p in slim_particles)

        assert slim_total < fat_total

    def test_all_particles_share_single_flyweight(self) -> None:
        shared = ParticleType("orange", "assets/fire_spark.png", 16, 16)
        particles = [
            Particle(particle_type=shared, x=float(i), y=float(i))
            for i in range(500)
        ]
        ids = {id(p.particle_type) for p in particles}
        assert len(ids) == 1
