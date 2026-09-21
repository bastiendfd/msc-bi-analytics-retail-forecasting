from pathlib import Path

from margin_analytics_lab.cli import main


def test_cli_writes_ranked_markdown_report(tmp_path: Path):
    source = tmp_path / "input.csv"
    output = tmp_path / "report.md"
    source.write_text(
        "category,revenue,cost\nTea,100,60\nCoffee,90,30\n", encoding="utf-8"
    )

    exit_code = main([str(source), str(output)])

    assert exit_code == 0
    assert output.read_text(encoding="utf-8") == (
        "# Category margin report\n\n"
        "| Rank | Category | Revenue | Cost | Margin | Margin rate |\n"
        "| ---: | --- | ---: | ---: | ---: | ---: |\n"
        "| 1 | Coffee | 90.00 | 30.00 | 60.00 | 66.67% |\n"
        "| 2 | Tea | 100.00 | 60.00 | 40.00 | 40.00% |\n"
    )
