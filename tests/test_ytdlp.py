import os
import pytest
import logging
from pathlib import Path

Log = logging.getLogger(__name__)


def get_percent_str(d):
    return d['_percent_str'].strip()[:-1]


def test_parsing_percent_str():
    Log.warning("---------------------------starting")
    txt = Path('d.json').read_text()


def parse_json_and_update_progressbar(d):
    extracted_string = get_percent_str(d)
    try:
        new_value = float(extracted_string) * 10
        return new_value
    except ValueError as e:
        Log.error("ValueError")
        raise e


@pytest.mark.skip(reason="no way of currently testing this")
def test_parsing_json():
    with open('d.json', 'r') as f:
        data = f.read()
    parse_json_and_update_progressbar(data)


"""
@pytest.fixture
def app(qtbot):
    test_hello_app = src.main.Window()
    qtbot.addWidget(test_hello_app)
    return test_hello_app
"""

if __name__ == '__main__':
    Log.info(' About to start the tests ')
    pytest.main(args=[os.path.abspath(__file__)])
    Log.info(' Done executing the tests ')
