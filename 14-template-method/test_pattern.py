# test_template_method.py - pytest verifying step order, customization, and extensibility
from __future__ import annotations

import pytest

from good_example import (
    CSVReport,
    HTMLReport,
    PDFReport,
    ReportGenerator,
    SalesRecord,
)


@pytest.fixture
def sample_records() -> list[SalesRecord]:
    return [
        SalesRecord("North", "Widget A", 15_000.00),
        SalesRecord("South", "Widget B", 23_500.50),
    ]


class TestStepOrder:
    def test_output_follows_title_body_summary_footer_sequence(
        self, sample_records: list[SalesRecord]
    ) -> None:
        report = PDFReport()
        output = report.generate(sample_records)
        lines = output.split("\n")
        assert lines[0].startswith("=== Sales Report")
        assert "Total Revenue" in output
        assert lines[-1] == "-- End of Report --"

    def test_step_methods_called_in_order(
        self, sample_records: list[SalesRecord]
    ) -> None:
        call_log: list[str] = []

        class SpyReport(ReportGenerator):
            def _title(self) -> str:
                call_log.append("title")
                return "Title"

            def _format_records(self, records: list[SalesRecord]) -> str:
                call_log.append("format_records")
                return "Body"

            def _format_total(self, total: float) -> str:
                call_log.append("format_total")
                return f"Total: {total}"

            def _footer(self) -> str:
                call_log.append("footer")
                return "Footer"

        SpyReport().generate(sample_records)
        assert call_log == ["title", "format_records", "format_total", "footer"]


class TestSubclassCustomization:
    def test_html_report_wraps_in_tags(
        self, sample_records: list[SalesRecord]
    ) -> None:
        output = HTMLReport().generate(sample_records)
        assert "<h1>" in output
        assert "<table>" in output
        assert "<footer>" in output

    def test_csv_report_uses_commas(
        self, sample_records: list[SalesRecord]
    ) -> None:
        output = CSVReport().generate(sample_records)
        assert "region,product,revenue" in output
        assert "# End of Report" in output

    def test_pdf_report_uses_fixed_width(
        self, sample_records: list[SalesRecord]
    ) -> None:
        output = PDFReport().generate(sample_records)
        assert "===" in output
        assert "Total Revenue: $" in output
