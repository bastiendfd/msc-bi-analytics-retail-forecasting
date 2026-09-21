from margin_analytics_lab.app import create_app


def test_dashboard_and_summary_api_expose_synthetic_kpis_and_forecast():
    app = create_app()
    client = app.test_client()

    response = client.get("/api/summary")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["data_notice"] == "All values are deterministic fictional data for education."
    assert payload["kpis"]["total_revenue"] > 0
    assert payload["margin_summary"]
    assert len(payload["forecast"]) == 7
    assert {"mae", "mape", "holdout_size"} == set(payload["evaluation"])
    assert client.get("/").status_code == 200
