# bad_example.py - HeavyImage loads the full file in __init__
import time


class HeavyImage:
    def __init__(self, path: str) -> None:
        self.path = path
        self.data = self._load_from_disk()

    def _load_from_disk(self) -> bytes:
        print(f"[HeavyImage] Loading {self.path} from disk...")
        time.sleep(0.5)  # simulate slow I/O
        return b"\x89PNG" * 1_000_000  # ~4 MB fake payload

    def display(self) -> str:
        return f"Displaying {self.path} ({len(self.data):,} bytes)"

    def get_path(self) -> str:
        return self.path


if __name__ == "__main__":
    gallery: list[HeavyImage] = [
        HeavyImage("photos/sunset.png"),
        HeavyImage("photos/mountain.png"),
        HeavyImage("photos/ocean.png"),
    ]
    print(gallery[0].display())
