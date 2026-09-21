from datetime import date

import pytest

from margin_analytics_lab.forecasting import (
    ForecastValidationError,
    evaluate_holdout,
    forecast_daily_sales,
)


def test_forecast_daily_sales_extends_deterministic_trend():
    history = [
        {"date": date(2026, 1, 1), "sales": 100.0},
        {"date": date(2026, 1, 2), "sales": 110.0},
        {"date": date(2026, 1, 3), "sales": 120.0},
    ]

    forecast = forecast_daily_sales(history, horizon=2)

    assert forecast == [
        {"date": date(2026, 1, 4), "sales_forecast": 130.0},
        {"date": date(2026, 1, 5), "sales_forecast": 140.0},
    ]


def test_forecast_rejects_history_with_missing_calendar_day():
    history = [
        {"date": date(2026, 1, 1), "sales": 100.0},
        {"date": date(2026, 1, 3), "sales": 120.0},
    ]

    with pytest.raises(ForecastValidationError, match="consecutive daily dates"):
        forecast_daily_sales(history)


def test_evaluate_holdout_returns_zero_error_for_linear_series():
    history = [
        {"date": date(2026, 1, day), "sales": float(100 + day * 10)}
        for day in range(1, 7)
    ]

    metrics = evaluate_holdout(history, holdout_size=2)

    assert metrics == {"mae": 0.0, "mape": 0.0, "holdout_size": 2}
