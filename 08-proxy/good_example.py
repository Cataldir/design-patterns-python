# good_example.py - virtual proxy + protection proxy
from __future__ import annotations

import time
from typing import Protocol


class ImageSubject(Protocol):
    def display(self) -> str: ...
    def get_path(self) -> str: ...


class RealImage:
    def __init__(self, path: str) -> None:
        self.path = path
        self.data = self._load_from_disk()

    def _load_from_disk(self) -> bytes:
        print(f"[RealImage] Loading {self.path} from disk...")
        time.sleep(0.5)
        return b"\x89PNG" * 1_000_000

    def display(self) -> str:
        return f"Displaying {self.path} ({len(self.data):,} bytes)"

    def get_path(self) -> str:
        return self.path


class ImageProxy:
    """Virtual proxy: defers RealImage creation until display() is called."""

    def __init__(self, path: str) -> None:
        self._path = path
        self._real: RealImage | None = None

    def display(self) -> str:
        if self._real is None:
            self._real = RealImage(self._path)
        return self._real.display()

    def get_path(self) -> str:
        return self._path


class ProtectedImage:
    """Protection proxy: checks user role before allowing display."""

    def __init__(self, wrapped: ImageSubject, role: str) -> None:
        self._wrapped = wrapped
        self._role = role

    def display(self) -> str:
        if self._role != "admin":
            raise PermissionError(
                f"Role '{self._role}' cannot display this image"
            )
        return self._wrapped.display()

    def get_path(self) -> str:
        return self._wrapped.get_path()
