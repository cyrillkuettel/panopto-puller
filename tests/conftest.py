from pathlib import Path

import pytest


@pytest.fixture
def absolute_base_path() -> Path:
    return Path(__file__).parent.resolve()


@pytest.fixture
def sample_cookie_path():
    return "/home/cyrill/Desktop/cookies.txt"


@pytest.fixture
def get_yaml_file(sample_cookie_path):
    absolute_file_path = sample_cookie_path
    return (
        "#Sample application configuration as if we have read the yaml from disk\n"
        f"absolute_file_path: {absolute_file_path}\n"
    )
