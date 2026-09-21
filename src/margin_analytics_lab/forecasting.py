"""Deterministic educational forecasting baseline for synthetic daily retail sales."""

from collections.abc import Mapping, Sequence
from datetime import date, timedelta
from math import isfinite


class ForecastValidationError(ValueError):
    """Raised when synthetic daily-sales history is not usable by the baseline."""


def _validated_history(rows: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    if len(rows) < 2:
        raise ForecastValidationError("at least two daily observations are required")
    normalized: list[dict[str, object]] = []
    previous_date: date | None = None
    for position, row in enumerate(rows, start=1):
        observed_date = row.get("date")
        if not isinstance(observed_date, date):
            raise ForecastValidationError(f"row {position}: date must be a date")
        try:
            sales = float(row["sales"])
        except (KeyError, TypeError, ValueError):
            raise ForecastValidationError(
                f"row {position}: sales must be a finite non-negative number"
            ) from None
        if not isfinite(sales) or sales < 0:
            raise ForecastValidationError(
                f"row {position}: sales must be a finite non-negative number"
            )
        if previous_date is not None and observed_date <= previous_date:
            raise ForecastValidationError("dates must be strictly increasing")
        if previous_date is not None and observed_date != previous_date + timedelta(days=1):
            raise ForecastValidationError("dates must be consecutive daily dates")
        normalized.append({"date": observed_date, "sales": sales})
        previous_date = observed_date
    return normalized


def _linear_coefficients(history: Sequence[Mapping[str, object]]) -> tuple[float, float]:
    count = len(history)
    x_mean = (count - 1) / 2
    y_mean = sum(float(row["sales"]) for row in history) / count
    denominator = sum((index - x_mean) ** 2 for index in range(count))
    slope = sum(
        (index - x_mean) * (float(row["sales"]) - y_mean)
        for index, row in enumerate(history)
    ) / denominator
    return y_mean - slope * x_mean, slope


def forecast_daily_sales(
    rows: Sequence[Mapping[str, object]], horizon: int = 7
) -> list[dict[str, object]]:
    """Forecast daily sales using an ordinary-least-squares time-index trend."""
    if horizon < 1:
        raise ForecastValidationError("horizon must be at least one day")
    history = _validated_history(rows)
    intercept, slope = _linear_coefficients(history)
    last_date = history[-1]["date"]
    assert isinstance(last_date, date)
    return [
        {
            "date": last_date + timedelta(days=step),
            "sales_forecast": round(max(0.0, intercept + slope * (len(history) + step - 1)), 2),
        }
        for step in range(1, horizon + 1)
    ]


def evaluate_holdout(
    rows: Sequence[Mapping[str, object]], holdout_size: int = 7
) -> dict[str, float | int]:
    """Evaluate the baseline with MAE and MAPE on the final synthetic observations."""
    history = _validated_history(rows)
    if holdout_size < 1 or holdout_size >= len(history):
        raise ForecastValidationError("holdout_size must be between one and len(rows) - 1")
    train, actual = history[:-holdout_size], history[-holdout_size:]
    predicted = forecast_daily_sales(train, horizon=holdout_size)
    errors = [
        abs(float(item["sales"]) - float(prediction["sales_forecast"]))
        for item, prediction in zip(actual, predicted, strict=True)
    ]
    mae = sum(errors) / holdout_size
    nonzero_actual = [float(item["sales"]) for item in actual if float(item["sales"]) > 0]
    mape = 0.0 if not nonzero_actual else sum(
        error / float(item["sales"]) * 100
        for item, error in zip(actual, errors, strict=True)
        if float(item["sales"]) > 0
    ) / len(nonzero_actual)
    return {"mae": round(mae, 2), "mape": round(mape, 2), "holdout_size": holdout_size}
