"""Deterministic validation for synthetic sales-and-cost rows."""

from collections.abc import Iterable, Mapping
from decimal import Decimal, InvalidOperation

REQUIRED_FIELDS = ("category", "revenue", "cost")


class DataValidationError(ValueError):
    """Raised when an input row is outside the documented CSV schema."""


def validate_rows(rows: Iterable[Mapping[str, str]]) -> list[dict[str, str]]:
    """Validate and normalize records without silently coercing bad values."""
    validated: list[dict[str, str]] = []
    for row_number, row in enumerate(rows, start=1):
        missing = [field for field in REQUIRED_FIELDS if field not in row]
        if missing:
            raise DataValidationError(
                f"row {row_number}: missing required fields: {', '.join(missing)}"
            )
        category = str(row["category"]).strip()
        if not category:
            raise DataValidationError(f"row {row_number}: category must not be blank")
        normalized = {"category": category}
        for field in ("revenue", "cost"):
            value = str(row[field]).strip()
            try:
                amount = Decimal(value)
            except (InvalidOperation, ValueError):
                raise DataValidationError(
                    f"row {row_number}: {field} must be a valid decimal"
                ) from None
            if not amount.is_finite():
                raise DataValidationError(f"row {row_number}: {field} must be a valid decimal")
            if amount < 0:
                raise DataValidationError(f"row {row_number}: {field} must be non-negative")
            normalized[field] = value
        validated.append(normalized)
    return validated
