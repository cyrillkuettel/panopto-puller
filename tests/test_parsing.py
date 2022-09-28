import logging
from pathlib import Path

from src.Utils import (
    string_to_dict,
    get_percent_str,
    get_new_progressbar_value,
    read_file_cookie_path,
    write_file_cookie_path
)

Log = logging.getLogger(__name__)


def test_extracting_percent_value_from_json():
    Log.warning("---------------------------starting")
    d = Path("d.json").read_text().strip()
    assert d not in ("", None)
    as_dict = string_to_dict(d)
    assert isinstance(as_dict, dict)
    assert "_percent_str" in as_dict


def test_parsing_json():
    yt_dlp_hook = Path(
        "d.json"
    ).read_text()  # information about the current download that we receive from yt-dlp
    yt_dlp_hook_dictionary = string_to_dict(yt_dlp_hook)
    extracted_percent_string = get_percent_str(yt_dlp_hook_dictionary)
    actual_length = len(extracted_percent_string)
    Log.error(f"extracted_percent_string = {extracted_percent_string}")
    assert actual_length <= 5  # for example: '100.0' as string
    assert actual_length >= 3
    value = get_new_progressbar_value(extracted_percent_string)
    assert 0 <= value <= 100


def test_parsing_yaml_for_cookie_path(get_yaml_file, sample_cookie_path):
    import yaml

    sample_config = get_yaml_file
    Log.error(sample_config)
    data = yaml.safe_load(sample_config)
    assert data["absolute_file_path"] == sample_cookie_path


def test_yaml_parsing(absolute_base_path):
    actual_config_path = absolute_base_path / "config.yaml"
    value_for_yaml = "/home/cyrill/cookies.txt"
    #  write some data to the config file
    write_file_cookie_path(config_file_path=actual_config_path,
                           value=value_for_yaml)
    #  read the data from config file
    new_absolute_cookie_path = read_file_cookie_path(
        config_file_path=actual_config_path
    )
    assert new_absolute_cookie_path == value_for_yaml
