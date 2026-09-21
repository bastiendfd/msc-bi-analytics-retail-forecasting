from decimal import Decimal

from margin_analytics_lab.reporting import build_category_report


def test_build_category_report_aggregates_and_ranks_categories():
    rows = [
        {"category": "Tea", "revenue": "100.00", "cost": "60.00"},
        {"category": "Tea", "revenue": "50.00", "cost": "35.00"},
        {"category": "Coffee", "revenue": "90.00", "cost": "30.00"},
    ]

    report = build_category_report(rows)

    assert report == [
        {
            "category": "Coffee",
            "revenue": Decimal("90.00"),
            "cost": Decimal("30.00"),
            "margin": Decimal("60.00"),
            "margin_rate": Decimal("66.67"),
        },
        {
            "category": "Tea",
            "revenue": Decimal("150.00"),
            "cost": Decimal("95.00"),
            "margin": Decimal("55.00"),
            "margin_rate": Decimal("36.67"),
        },
    ]


def test_build_category_report_sets_zero_rate_when_revenue_is_zero():
    report = build_category_report([{"category": "Samples", "revenue": "0", "cost": "0"}])

    assert report[0]["margin_rate"] == Decimal("0.00")
