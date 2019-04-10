import pytest
import os
from py_repo import PyRepo


@pytest.fixture
def dummy_py_repo():
    return PyRepo("tensorflow", "tensorflow/models", None, None, None, None, None, None, None)


@pytest.fixture
def output_directory():
    return "./"


@pytest.fixture
def target_file_directory():
    return "./tensorflow/models/test.txt"


def test_reject_file_exist(dummy_py_repo, output_directory, target_file_directory):
    os.mkdir("./tensorflow")
    os.mkdir("./tensorflow/models")
    open(target_file_directory, "w+").close()
    dummy_py_repo.reject(output_directory)
    exist = os.path.exists(target_file_directory)
    assert not exist
    import shutil
    shutil.rmtree("./tensorflow")


def test_reject_file_not_exist(dummy_py_repo, output_directory, target_file_directory):
    dummy_py_repo.reject(output_directory)
    exist = os.path.exists(target_file_directory)
    assert not exist



