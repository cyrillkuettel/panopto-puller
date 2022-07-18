import os
import pytest
import logging
from pathlib import Path
import json

Log = logging.getLogger(__name__)


def string_to_dict(d):
    json1_data: dict = json.loads(d)
    return json1_data


def test_extracting_percent_value_from_json():
    Log.warning("---------------------------starting")
    d = Path('d.json').read_text().strip()
    assert d not in ('', None)
    as_dict = string_to_dict(d)
    assert isinstance(as_dict, dict)
    assert '_percent_str' in as_dict


def get_new_progressbar_value(percent):
    try:
        new_progressbar_value = int(float(percent))
        return new_progressbar_value
    except ValueError as e:
        Log.error("ValueError. Raising the exception")
        raise e


def get_percent_str(d):
    percent_text = d['_percent_str']
    left_text = percent_text.partition("%")[0]
    n = len(left_text)
    return left_text[n - 5:n]


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



