"""Command-line interface for synthetic category margin reports."""

import argparse
import csv
from collections.abc import Sequence
from pathlib import Path

from .reporting import build_category_report
from .validation import validate_rows


def render_markdown(report: list[dict[str, object]]) -> str:
    """Render a ranked report as a stable Markdown table."""
    lines = [
        "# Category margin report",
        "",
        "| Rank | Category | Revenue | Cost | Margin | Margin rate |",
        "| ---: | --- | ---: | ---: | ---: | ---: |",
    ]
    for rank, item in enumerate(report, start=1):
        lines.append(
            "| {rank} | {category} | {revenue:.2f} | {cost:.2f} | {margin:.2f} | "
            "{margin_rate:.2f}% |".format(rank=rank, **item)
        )
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    """Read a CSV, validate it, and write a ranked Markdown report."""
    parser = argparse.ArgumentParser(description="Create a synthetic category margin report.")
    parser.add_argument("input_csv", type=Path, help="CSV with category,revenue,cost columns")
    parser.add_argument("output_markdown", type=Path, help="Destination Markdown file")
    args = parser.parse_args(argv)

    with args.input_csv.open("r", encoding="utf-8", newline="") as source:
        rows = validate_rows(csv.DictReader(source))
    args.output_markdown.write_text(render_markdown(build_category_report(rows)), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
