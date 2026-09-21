"""Deterministic, generic synthetic retail fixture used only for local demonstrations."""

from datetime import date, timedelta


def synthetic_daily_sales(days: int = 42) -> list[dict[str, object]]:
    """Return a reproducible daily-sales series with trend and weekly seasonality."""
    if days < 2:
        raise ValueError("days must be at least two")
    start = date(2026, 1, 1)
    weekly_effect = (0, 5, 8, 4, 10, 18, 12)
    return [
        {
            "date": start + timedelta(days=index),
            "sales": float(240 + index * 3 + weekly_effect[index % len(weekly_effect)]),
        }
        for index in range(days)
    ]


def synthetic_margin_rows() -> list[dict[str, str]]:
    """Return generic fictional category rows compatible with the margin report."""
    return [
        {"category": "Home goods", "revenue": "1260.00", "cost": "790.00"},
        {"category": "Pantry", "revenue": "980.00", "cost": "610.00"},
        {"category": "Personal care", "revenue": "840.00", "cost": "490.00"},
    ]
