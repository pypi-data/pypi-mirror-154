"""Unit tests for the Notional parsers."""

from notional import schema, types
from notional.parser import CsvParser


def test_basic_csv_data_check():
    """Confirm basic CSV data pasring."""

    data = """first,last\none,two"""

    parser = CsvParser(header_row=True)
    parser.parse(data)

    assert "first" in parser.schema
    assert isinstance(parser.schema["first"], schema.Title)

    assert "last" in parser.schema
    assert isinstance(parser.schema["last"], schema.RichText)

    assert len(parser.content) == 1

    entry = parser.content[0]

    assert "first" in entry
    assert isinstance(entry["first"], types.Title)
    assert entry["first"].Value == "one"

    assert "last" in entry
    assert isinstance(entry["last"], types.RichText)
    assert entry["last"].Value == "two"
