# good_example.py - Template Method with ABC, abstract steps, and optional hooks
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class SalesRecord:
    region: str
    product: str
    revenue: float


class ReportGenerator(ABC):
    def generate(self, records: list[SalesRecord]) -> str:
        """Template method \u2014 defines the invariant algorithm skeleton."""
        parts: list[str] = [
            self._title(),
            self._format_records(records),
            self._summary(records),
            self._footer(),
        ]
        return "\n".join(parts)

    @abstractmethod
    def _title(self) -> str: ...

    @abstractmethod
    def _format_records(self, records: list[SalesRecord]) -> str: ...

    def _summary(self, records: list[SalesRecord]) -> str:
        total = sum(r.revenue for r in records)
        return self._format_total(total)

    @abstractmethod
    def _format_total(self, total: float) -> str: ...

    def _footer(self) -> str:
        return "-- End of Report --"


class PDFReport(ReportGenerator):
    def _title(self) -> str:
        return "=== Sales Report (PDF) ==="

    def _format_records(self, records: list[SalesRecord]) -> str:
        lines = [
            f"  {r.region:<12} {r.product:<15} ${r.revenue:>10,.2f}"
            for r in records
        ]
        return "\n".join(lines)

    def _format_total(self, total: float) -> str:
        return f"Total Revenue: ${total:,.2f}"


class HTMLReport(ReportGenerator):
    def _title(self) -> str:
        return "<h1>Sales Report (HTML)</h1>"

    def _format_records(self, records: list[SalesRecord]) -> str:
        rows = [
            f"  <tr><td>{r.region}</td><td>{r.product}</td>"
            f"<td>${r.revenue:,.2f}</td></tr>"
            for r in records
        ]
        return "<table>\n" + "\n".join(rows) + "\n</table>"

    def _format_total(self, total: float) -> str:
        return f"<p>Total Revenue: ${total:,.2f}</p>"

    def _footer(self) -> str:
        return "<footer>End of Report</footer>"


class CSVReport(ReportGenerator):
    def _title(self) -> str:
        return "# Sales Report (CSV)"

    def _format_records(self, records: list[SalesRecord]) -> str:
        header = "region,product,revenue"
        rows = [f"{r.region},{r.product},{r.revenue:.2f}" for r in records]
        return "\n".join([header] + rows)

    def _format_total(self, total: float) -> str:
        return f"# Total Revenue: {total:.2f}"

    def _footer(self) -> str:
        return "# End of Report"


if __name__ == "__main__":
    data = [
        SalesRecord("North", "Widget A", 15_000.00),
        SalesRecord("South", "Widget B", 23_500.50),
        SalesRecord("East", "Widget A", 18_750.25),
    ]
    for report_cls in (PDFReport, HTMLReport, CSVReport):
        print(report_cls().generate(data))
        print()
