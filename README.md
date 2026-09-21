# MSc Business Intelligence & Analytics — Synthetic Retail Forecasting Lab

A compact, deterministic Python lab that supports an MSc Business Intelligence & Analytics portfolio: it combines a retained category-margin CLI with a transparent daily-sales forecasting baseline and a local-only Flask dashboard/API.

> **Fictional-data notice:** every value, category, and time series in this repository is invented, generic, and deterministic. Nothing here comes from customers, retailers, suppliers, people, transactions, or external systems.

## Scope and honest limitations

- This is an **educational baseline**, not retail, financial, accounting, or demand-forecasting software.
- Its linear time-index regression is deliberately simple; it does not model promotions, price, stockouts, holidays, weather, hierarchy, uncertainty, drift, or operational constraints.
- Evaluation is only an in-sample synthetic holdout (MAE and MAPE), not evidence of real-world performance.
- The dashboard is a local demonstration with no authentication, authorization, persistence, deployment configuration, or production hardening.
- Do not use its outputs for financial reporting, pricing, staffing, purchasing, inventory, or other decisions.

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
.venv/Scripts/python -m pip install --upgrade pip
.venv/Scripts/python -m pip install -e ".[dev]"
```

### Margin CLI

```bash
margin-report data/sample_sales.csv report.md
```

This writes a ranked, generic category-margin table.

### Forecast CLI

```bash
synthetic-forecast forecast-summary.json --horizon 7
```

This writes deterministic fictional daily forecasts and holdout MAE/MAPE to JSON. Generated output is intentionally ignored by Git.

### Local dashboard and API

```bash
synthetic-dashboard
```

The command is deliberately fixed to `http://127.0.0.1:5000` with `debug=False`. Open `/` for the minimal page or request `http://127.0.0.1:5000/api/summary` for JSON. Stop it with `Ctrl+C`; it is not a deployment command.

## Architecture

```text
synthetic.py ──> forecasting.py ──> forecast_cli.py ──> JSON export
      │                 │
      └──> reporting.py ┴──> app.py ──> dashboard.py ──> localhost Flask UI/API
                         │
                    validation.py ──> cli.py ──> Markdown margin report
```

- `synthetic.py` provides reproducible generic fixtures only.
- `forecasting.py` validates consecutive daily observations, fits ordinary least squares against a day index, and computes MAE/MAPE on a final holdout.
- `reporting.py` and `validation.py` retain the existing decimal-based category-margin demonstration.
- `app.py` exposes aggregated KPI, margin, forecast, and evaluation summaries without reading external data.

## Data and model cards

See [DATA_CARD.md](DATA_CARD.md) for fixture provenance and [MODEL_CARD.md](MODEL_CARD.md) for baseline design, evaluation, and limitations. See [SECURITY.md](SECURITY.md) for responsible disclosure.

## Development and verification

```bash
python -m pytest -q
python -m ruff check .
python -m compileall -q src
```

CI runs the same test, lint, and compile checks on Python 3.11. Dependabot checks Python and GitHub Actions dependencies weekly.
