"""Entrypoint for the intentionally local-only educational dashboard."""

from collections.abc import Sequence

from .app import create_app


def server_options() -> dict[str, str | int | bool]:
    """Return fixed safe local-development options, never a production configuration."""
    return {"host": "127.0.0.1", "port": 5000, "debug": False}


def main(argv: Sequence[str] | None = None) -> int:
    """Run the dashboard only on the local loopback interface."""
    if argv:
        raise SystemExit("dashboard accepts no arguments")
    create_app().run(**server_options())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
