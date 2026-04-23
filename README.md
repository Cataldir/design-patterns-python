# Design Patterns in Python — Companion Repository

Code examples for the Udemy course **Design Patterns with Python: A Practical Guide**.

## Structure

Each pattern has its own folder with three files:

| File | Purpose |
|------|---------|
| `bad_example.py` | The problem — code that works but violates design principles |
| `good_example.py` | The pattern applied — clean, extensible implementation |
| `test_pattern.py` | Tests proving both versions produce the same output |

## Patterns Covered

### Creational

| # | Pattern | Folder |
|---|---------|--------|
| 1 | Factory Method | `01-factory/` |
| 2 | Abstract Factory | `02-abstract-factory/` |
| 3 | Prototype | `03-prototype/` |
| 4 | Builder | `04-builder/` |

### Structural

| # | Pattern | Folder |
|---|---------|--------|
| 5 | Adapter | `05-adapter/` |
| 6 | Bridge | `06-bridge/` |
| 7 | Flyweight | `07-flyweight/` |
| 8 | Proxy | `08-proxy/` |
| 9 | Facade | `09-facade/` |

### Behavioral

| # | Pattern | Folder |
|---|---------|--------|
| 10 | Command | `10-command/` |
| 11 | Strategy | `11-strategy/` |
| 12 | State | `12-state/` |
| 13 | Observer | `13-observer/` |
| 14 | Template Method | `14-template-method/` |
| 15 | Iterator | `15-iterator/` |

## Labs

| Lab | Folder | Patterns |
|-----|--------|----------|
| L1 | `labs/lab-L1-strategy-refactor/` | Strategy |
| L2 | `labs/lab-L2-command-observer-pipeline/` | Command + Observer |
| L3 | `labs/lab-L3-ai-pattern-discovery/` | AI-assisted discovery |

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Running Tests

```bash
pytest -v
```

## Requirements

- Python 3.11+
- pytest

## License

MIT
