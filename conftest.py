import sys
from pathlib import Path

_PATTERN_MODULES = frozenset({"good_example", "bad_example"})


def _activate_pattern_dir(d: str) -> None:
    """Evict stale pattern modules and put *d* first on sys.path."""
    for name in _PATTERN_MODULES:
        sys.modules.pop(name, None)
    if d in sys.path:
        sys.path.remove(d)
    sys.path.insert(0, d)


def pytest_collect_file(parent, file_path: Path):  # type: ignore[override]
    """Ensure each test directory resolves its own good_example / bad_example."""
    if file_path.suffix == ".py" and file_path.name.startswith("test_"):
        _activate_pattern_dir(str(file_path.parent))
    return None


def pytest_runtest_setup(item):  # type: ignore[no-untyped-def]
    """Re-activate the correct pattern dir before each test runs."""
    _activate_pattern_dir(str(item.path.parent))
