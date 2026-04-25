# test_factory.py — Pytest parametrized tests for the factory
import pytest

from good_example import _REGISTRY, create_exporter


@pytest.mark.parametrize("format_type", list(_REGISTRY))
def test_create_exporter_returns_valid_instance(format_type: str) -> None:
    exporter = create_exporter(format_type, title="Test")
    result = exporter.export("sample data")
    assert isinstance(result, str)
    assert len(result) > 0


def test_pdf_exporter_output() -> None:
    exporter = create_exporter("pdf", title="Report")
    assert exporter.export("data") == "[PDF] Report: data"


def test_csv_exporter_output() -> None:
    exporter = create_exporter("csv", title="Report")
    assert exporter.export("data") == "title,content\nReport,data"


def test_unknown_format_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Unknown format: xml"):
        create_exporter("xml", title="Report")
