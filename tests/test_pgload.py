import pytest
import pgload


def test_validate_data(capsys):
    pgload.validate_data(
        {
            "data": [{"id": 1, "name": "tim"}],
            "type": {"id": "bigint", "name": "character"},
            "index": ["id"],
            "unique": "id",
            "schema": "testdata",
            "table": "table01",
        }
    )
    captured = capsys.readouterr()
    print(
        "----------------------------------------------------------------------------------------"
    )
    print(captured)
    print(
        "----------------------------------------------------------------------------------------"
    )
    assert (
        "Missing top level key(s) found: ['index', 'schema', 'table', 'unique']. Please add."
        in captured.out
    )
