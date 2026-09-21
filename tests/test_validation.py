import pytest

from margin_analytics_lab.validation import DataValidationError, validate_rows


def test_validate_rows_rejects_missing_required_field():
    with pytest.raises(DataValidationError, match="missing required fields: cost"):
        validate_rows([{"category": "Tea", "revenue": "10.00"}])


def test_validate_rows_rejects_negative_amount():
    with pytest.raises(DataValidationError, match="revenue must be non-negative"):
        validate_rows([{"category": "Tea", "revenue": "-1", "cost": "0"}])


def test_validate_rows_rejects_invalid_decimal():
    with pytest.raises(DataValidationError, match="cost must be a valid decimal"):
        validate_rows([{"category": "Tea", "revenue": "10", "cost": "unknown"}])


def test_validate_rows_normalizes_valid_rows():
    assert validate_rows([{"category": "  Tea  ", "revenue": "10", "cost": "4.5"}]) == [
        {"category": "Tea", "revenue": "10", "cost": "4.5"}
    ]
