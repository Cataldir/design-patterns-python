# bad_example.py - Three report functions duplicating the same algorithm skeleton
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SalesRecord:
    region: str
    product: str
    revenue: float


def generate_pdf_report(records: list[SalesRecord]) -> str:
    lines: list[str] = []
    lines.append("=== Sales Report (PDF) ===")
    lines.append("")
    for r in records:
        lines.append(f"  {r.region:<12} {r.product:<15} ${r.revenue:>10,.2f}")
    lines.append("")
    total = sum(r.revenue for r in records)
    lines.append(f"Total Revenue: ${total:,.2f}")
    lines.append("=== End of Report ===")
    return "\n".join(lines)


def generate_html_report(records: list[SalesRecord]) -> str:
    lines: list[str] = []
    lines.append("<h1>Sales Report (HTML)</h1>")
    lines.append("<table>")
    for r in records:
        lines.append(
            f"  <tr><td>{r.region}</td><td>{r.product}</td>"
            f"<td>${r.revenue:,.2f}</td></tr>"
        )
    lines.append("</table>")
    total = sum(r.revenue for r in records)
    lines.append(f"<p>Total Revenue: ${total:,.2f}</p>")
    lines.append("<footer>End of Report</footer>")
    return "\n".join(lines)


def generate_csv_report(records: list[SalesRecord]) -> str:
    lines: list[str] = []
    lines.append("# Sales Report (CSV)")
    lines.append("region,product,revenue")
    for r in records:
        lines.append(f"{r.region},{r.product},{r.revenue:.2f}")
    total = sum(r.revenue for r in records)
    lines.append(f"# Total Revenue: {total:.2f}")
    lines.append("# End of Report")
    return "\n".join(lines)


if __name__ == "__main__":
    data = [
        SalesRecord("North", "Widget A", 15_000.00),
        SalesRecord("South", "Widget B", 23_500.50),
        SalesRecord("East", "Widget A", 18_750.25),
    ]
    print(generate_pdf_report(data))
