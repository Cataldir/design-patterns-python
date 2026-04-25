# bad_example.py — If-else chain couples callers to every concrete exporter
from dataclasses import dataclass


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


def run(format_type: str, title: str, data: str) -> str:
    """Every new format forces edits here — violates OCP."""
    if format_type == "pdf":
        exporter = PDFExporter(title=title)
    elif format_type == "csv":
        exporter = CSVExporter(title=title)
    elif format_type == "html":
        exporter = HTMLExporter(title=title)
    else:
        raise ValueError(f"Unknown format: {format_type}")
    return exporter.export(data)


if __name__ == "__main__":
    for fmt in ["pdf", "csv", "html"]:
        print(run(fmt, "Sales Report", "Q1 revenue: $1.2M"))
