from margin_analytics_lab.dashboard import server_options


def test_dashboard_server_options_are_localhost_without_debug():
    assert server_options() == {"host": "127.0.0.1", "port": 5000, "debug": False}
