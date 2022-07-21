from pathlib import Path

import pytest

from src.Utils import *

Log = logging.getLogger(__name__)


def test_extracting_percent_value_from_json():
    Log.warning("---------------------------starting")
    d = Path('d.json').read_text().strip()
    assert d not in ('', None)
    as_dict = string_to_dict(d)
    assert isinstance(as_dict, dict)
    assert '_percent_str' in as_dict


def test_parsing_json():
    yt_dlp_hook = Path('d.json').read_text()  # information about the current download that we receive from yt-dlp
    yt_dlp_hook_dictionary = string_to_dict(yt_dlp_hook)
    extracted_percent_string = get_percent_str(yt_dlp_hook_dictionary)
    actual_length = len(extracted_percent_string)
    Log.error(f"extracted_percent_string = {extracted_percent_string}")
    assert actual_length <= 5  # for example: '100.0' as string
    assert actual_length >= 3
    value = get_new_progressbar_value(extracted_percent_string)
    assert 0 <= value <= 100


@pytest.fixture
def sample_cookie_path():
    return "/home/cyrill/Desktop/cookies.txt"


@pytest.fixture
def get_yaml_file(sample_cookie_path):
    absolute_file_path = sample_cookie_path
    return (
        '#Sample application configuration as if we have read the yaml from disk\n'
        f'absolute_file_path: {absolute_file_path}\n'
    )


def test_parsing_yaml_for_cookie_path(get_yaml_file, sample_cookie_path):
    import yaml
    sample_config = get_yaml_file
    Log.error(sample_config)
    data = yaml.safe_load(sample_config)
    assert data['absolute_file_path'] == sample_cookie_path
