# Data Card — Synthetic Retail Fixtures

## Purpose

The fixtures exercise a generic margin-analysis workflow and a deterministic daily-sales forecasting baseline.

## Provenance

Every value and category in this repository was independently invented for this repository. The data are not collected from people, customers, suppliers, retailers, transactions, or external systems. They contain no personal data, credentials, identifiers, locations, invoices, or real business metrics.

## Contents

- `data/sample_sales.csv`: a small generic category fixture with positive decimal revenue and cost values.
- `synthetic_daily_sales()`: generated in-memory daily values with a documented trend plus a fixed repeating weekly effect.
- `synthetic_margin_rows()`: generated in-memory generic category revenue/cost values.

No generated dataset needs to be committed; generated datasets and outputs are ignored by Git.

## Limitations and responsible use

- The data are fictional and unsuitable for inference about any company, market, customer, product, or financial outcome.
- They omit taxes, returns, rebates, discounts, inventory, currency, accounting periods, promotions, stockouts, and audit controls.
- Calculations and forecasts are educational demonstrations, not accounting, retail, or financial forecasting software.
- Validate, govern, and document any real-world data independently before using analytic outputs.
