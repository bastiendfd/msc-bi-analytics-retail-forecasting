"""CLI for exporting the deterministic synthetic forecasting summary."""

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from .forecasting import evaluate_holdout, forecast_daily_sales
from .synthetic import synthetic_daily_sales


def main(argv: Sequence[str] | None = None) -> int:
    """Write local educational forecast and holdout metrics as JSON."""
    parser = argparse.ArgumentParser(
        description="Forecast deterministic synthetic retail daily sales."
    )
    parser.add_argument("output_json", type=Path, help="Destination JSON file")
    parser.add_argument(
        "--horizon", type=int, default=7, help="Number of daily forecasts (default: 7)"
    )
    args = parser.parse_args(argv)
    history = synthetic_daily_sales()
    payload = {
        "data_notice": "All values are deterministic fictional data for education.",
        "forecast": [
            {"date": item["date"].isoformat(), "sales_forecast": item["sales_forecast"]}
            for item in forecast_daily_sales(history, horizon=args.horizon)
        ],
        "evaluation": evaluate_holdout(history, holdout_size=7),
    }
    args.output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
