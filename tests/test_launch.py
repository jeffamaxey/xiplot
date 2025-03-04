import time

from xiplot.setup import setup_xiplot_dash_app


def test_dash001_launch(dash_duo):
    driver = dash_duo.driver
    dash_duo.start_server(setup_xiplot_dash_app())
    time.sleep(1)
    dash_duo.wait_for_page()

    assert dash_duo.get_logs() == [], "browser console should contain no error"
