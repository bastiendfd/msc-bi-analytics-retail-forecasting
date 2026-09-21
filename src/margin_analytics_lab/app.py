"""Local-only Flask views for the synthetic educational dashboard."""

from decimal import Decimal

from flask import Flask, jsonify, render_template_string

from .forecasting import evaluate_holdout, forecast_daily_sales
from .reporting import build_category_report
from .synthetic import synthetic_daily_sales, synthetic_margin_rows

NOTICE = "All values are deterministic fictional data for education."

_PAGE = """<!doctype html>
<title>Synthetic Retail Forecasting Lab</title>
<h1>Synthetic Retail Forecasting Lab</h1>
<p><strong>Educational local demo only.</strong> {{ notice }}</p>
<p>Use <a href=\"/api/summary\">/api/summary</a> for the JSON summary.</p>
"""


def _decimal_as_float(value: Decimal | str) -> float | str:
    return float(value) if isinstance(value, Decimal) else value


def build_summary() -> dict[str, object]:
    """Assemble deterministic local dashboard payload from generic synthetic fixtures."""
    margin_summary = [
        {key: _decimal_as_float(value) for key, value in item.items()}
        for item in build_category_report(synthetic_margin_rows())
    ]
    total_revenue = sum(float(item["revenue"]) for item in margin_summary)
    total_margin = sum(float(item["margin"]) for item in margin_summary)
    daily_sales = synthetic_daily_sales()
    forecast = forecast_daily_sales(daily_sales, horizon=7)
    return {
        "data_notice": NOTICE,
        "kpis": {
            "total_revenue": round(total_revenue, 2),
            "total_margin": round(total_margin, 2),
            "margin_rate": round(total_margin / total_revenue * 100, 2),
        },
        "margin_summary": margin_summary,
        "forecast": [
            {"date": item["date"].isoformat(), "sales_forecast": item["sales_forecast"]}
            for item in forecast
        ],
        "evaluation": evaluate_holdout(daily_sales, holdout_size=7),
    }


def create_app() -> Flask:
    """Create a local-only dashboard application; hosting is configured by the CLI."""
    app = Flask(__name__)

    @app.get("/")
    def dashboard() -> str:
        return render_template_string(_PAGE, notice=NOTICE)

    @app.get("/api/summary")
    def summary():
        return jsonify(build_summary())

    return app
