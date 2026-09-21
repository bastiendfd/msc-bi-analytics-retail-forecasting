# Margin Analytics Lab

A small, deterministic Python CLI that demonstrates category-level revenue, cost, gross-margin, and margin-rate calculations from a CSV file.

> **Fictional-data notice:** the included sample data is entirely synthetic and uses generic categories. This project is a demonstration only and is **not accounting software**. Do not use it for financial reporting, tax, audit, pricing, or operational decisions.

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
.venv/Scripts/python -m pip install --upgrade pip
.venv/Scripts/python -m pip install . pytest ruff
margin-report data/sample_sales.csv report.md
```

On macOS/Linux, activate or invoke the environment using the platform-appropriate path. The command writes a ranked Markdown table to `report.md`.

## Input schema

The CSV must include these required header fields. Additional headers are allowed and ignored:

| Field | Meaning | Rules |
| --- | --- | --- |
| `category` | Generic product category | Non-blank text |
| `revenue` | Synthetic revenue value | Finite, non-negative decimal |
| `cost` | Synthetic cost value | Finite, non-negative decimal |

Rows are aggregated by category. Gross margin is `revenue - cost`; margin rate is `(margin / revenue) * 100`, rounded to two decimals. A category with zero revenue receives a `0.00%` margin rate to avoid division by zero.

## Development

```bash
.venv/Scripts/python -m pytest -q
.venv/Scripts/python -m ruff check .
```

See [DATA_CARD.md](DATA_CARD.md) for scope and limitations, and [SECURITY.md](SECURITY.md) for vulnerability reporting.
