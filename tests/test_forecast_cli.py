import json
from pathlib import Path

from margin_analytics_lab.forecast_cli import main


def test_forecast_cli_writes_deterministic_summary(tmp_path: Path):
    output = tmp_path / "forecast.json"

    exit_code = main([str(output), "--horizon", "3"])

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert len(payload["forecast"]) == 3
    assert payload["evaluation"]["holdout_size"] == 7
