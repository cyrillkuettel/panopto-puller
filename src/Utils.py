import json
import yaml
import logging
from pathlib import Path

Log = logging.getLogger(__name__)


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
    percent_text = d["_percent_str"]
    left_text = percent_text.partition("%")[0]
    n = len(left_text)
    return left_text[n - 5 : n]


def string_to_dict(d):
    json1_data: dict = json.loads(d)
    return json1_data


def create_dir_if_not_exists(base_path: Path, conf_file_name: str):
    config_file_to_write = base_path / conf_file_name
    with open(config_file_to_write, "a+") as f:
        f.write("# configurations for downloader. Do not move this file. \n")


def write_file_cookie_path(config_file_path: Path, value: str):
    try:
        with open(str(config_file_path)) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        data["absolute_file_path"] = value
        with open(config_file_path, "w") as f:
            yaml.dump(data, f)
    except IOError as err:
        Log.error(
            f"failed persist_cookie_path in Path {config_file_path} and value {value}"
        )
        Log.error(err)


def read_file_cookie_path(config_file_path: Path):
    try:
        with open(str(config_file_path)) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data["absolute_file_path"]
    except IOError as err:
        Log.error(f"failed persist_cookie_path in Path {config_file_path}")
        Log.error(err)
