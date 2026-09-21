# Model Card — Synthetic Linear Trend Baseline

## Intended use

This model is a transparent teaching example for fitting and evaluating a simple forecast against a **deterministic fictional** daily-sales series. It is intended for code reading, testing, and local demonstrations only.

## Method

`forecast_daily_sales` validates at least two strictly consecutive daily observations, then fits ordinary least squares using observation index as the sole feature. Forecasts are extrapolated for the requested horizon and clipped at zero. The model uses only the Python standard library; there are no external data, trained artifacts, model files, or hidden parameters.

## Evaluation

`evaluate_holdout` reserves the final seven synthetic observations by default, trains on the earlier fixture rows, then returns:

- **MAE** — mean absolute error in the synthetic sales unit.
- **MAPE** — mean absolute percentage error, excluding zero actual values.

Metrics are calculated only on the repository's synthetic fixture. They do not validate performance on a retailer, product, geography, customer segment, or real time period.

## Limitations and risks

- Linear trend extrapolation is fragile and intentionally omits seasonality features, promotions, price, holidays, stockouts, returns, assortment changes, and uncertainty intervals.
- It has no backtesting pipeline beyond one final synthetic holdout, no monitoring, no drift detection, and no calibration.
- Results are not suitable for forecasting demand, revenue, margin, cash flow, inventory, purchasing, pricing, or financial outcomes.
- A real use case requires governed data, a clearly defined target, leakage controls, appropriate validation, uncertainty estimates, bias/risk assessment, monitoring, and domain review.
