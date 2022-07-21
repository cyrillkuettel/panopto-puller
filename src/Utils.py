import json
import logging
from pathlib import Path

Log = logging.getLogger(__name__)

conf_file_name = "config.yaml"


def get_new_value(yt_dlp_hook_dictionary) -> int:
    """
    :param d: Current progress hook from youtube-dl (information in json)
    :return: The value to be written in the progress bar
    """
    # yt_dlp_hook_dictionary = string_to_dict(d)
    extracted_percent_string = get_percent_str(yt_dlp_hook_dictionary)
    value = get_new_progressbar_value(extracted_percent_string)
    return value


def get_new_progressbar_value(percent) -> int:
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


def string_to_dict(d):
    json1_data: dict = json.loads(d)
    return json1_data


def create_dir_if_not_exists(base_path: Path):
    config_file_to_write: Path = base_path / conf_file_name
    with open(config_file_to_write, "a+") as f:
        f.write("# configurations for downloader. Do not move this file. \n")
