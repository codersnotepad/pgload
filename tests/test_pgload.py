import pytest
import pgload


def test_validate_data(capsys):
    pgload.validate_data(
        {
            "data": [{"id": 1, "name": "tim"}],
            "type": {"id": "bigint", "name": "character"},
            "index": ["id"],
            "unique": ["id"],
            "schema": {"name":"testdata", "owner":"tim", "grant":{"usage":"group02","all":"group01"}},
            "table": {"name":"table01", "owner":"tim", "grant":{"all":"group01"}},
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
        ""
        in captured.out
    )
