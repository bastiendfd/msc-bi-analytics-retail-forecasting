"""Category-level revenue, cost, and margin calculations."""

from collections import defaultdict
from collections.abc import Iterable, Mapping
from decimal import ROUND_HALF_UP, Decimal

CENTS = Decimal("0.01")


def build_category_report(rows: Iterable[Mapping[str, str]]) -> list[dict[str, Decimal | str]]:
    """Aggregate rows by category and rank by gross margin descending."""
    totals: dict[str, dict[str, Decimal]] = defaultdict(
        lambda: {"revenue": Decimal(0), "cost": Decimal(0)}
    )
    for row in rows:
        category = str(row["category"])
        totals[category]["revenue"] += Decimal(str(row["revenue"]))
        totals[category]["cost"] += Decimal(str(row["cost"]))

    report = []
    for category, values in totals.items():
        revenue = values["revenue"].quantize(CENTS)
        cost = values["cost"].quantize(CENTS)
        margin = (revenue - cost).quantize(CENTS)
        margin_rate = (
            Decimal("0.00")
            if revenue == 0
            else (margin / revenue * 100).quantize(CENTS, rounding=ROUND_HALF_UP)
        )
        report.append(
            {
                "category": category,
                "revenue": revenue,
                "cost": cost,
                "margin": margin,
                "margin_rate": margin_rate,
            }
        )
    return sorted(report, key=lambda item: (-item["margin"], item["category"]))
