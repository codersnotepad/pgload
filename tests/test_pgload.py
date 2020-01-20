import pytest
import pgload


def test_validate_data(capsys):
    pgload.validate_data({"data": [{"id": 1, "name": "tim"}]})
    captured = capsys.readouterr()
    assert "Jall" in captured.out
