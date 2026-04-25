# good_example.py — Factory dispatch with Protocol and registry
from dataclasses import dataclass
from typing import Protocol


class Exporter(Protocol):
    def export(self, data: str) -> str: ...


@dataclass
class PDFExporter:
    title: str

    def export(self, data: str) -> str:
        return f"[PDF] {self.title}: {data}"


@dataclass
class CSVExporter:
    title: str

    def export(self, data: str) -> str:
        header = "title,content"
        return f"{header}\n{self.title},{data}"


@dataclass
class HTMLExporter:
    title: str

    def export(self, data: str) -> str:
        return f"<html><h1>{self.title}</h1><p>{data}</p></html>"


_REGISTRY: dict[str, type[Exporter]] = {
    "pdf": PDFExporter,
    "csv": CSVExporter,
    "html": HTMLExporter,
}


def create_exporter(format_type: str, title: str) -> Exporter:
    cls = _REGISTRY.get(format_type)
    if cls is None:
        raise ValueError(f"Unknown format: {format_type}")
    return cls(title=title)


def run(format_type: str, title: str, data: str) -> str:
    return create_exporter(format_type, title).export(data)


if __name__ == "__main__":
    for fmt in ["pdf", "csv", "html"]:
        print(run(fmt, "Sales Report", "Q1 revenue: $1.2M"))
