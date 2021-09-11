import glob
import os

import pytest

from .utils import assert_like, process_all


def simple_name(filename):
    return os.path.splitext(os.path.basename(filename))[0]


path = os.path.dirname(os.path.realpath(__file__))
files = [
    pytest.param(f, id=simple_name(f))
    for f in glob.glob(path + "/samples/**/*.yml", recursive=True)
]

os.environ["YGLU_ENABLE_ENV"] = "true"


@pytest.mark.parametrize("filename", files)
def test_sample(filename):
    with open(filename) as file_handle:
        (input, output) = process_all(file_handle, filename, FailingErrorHandler())
        assert_like(input, output)

class FailingErrorHandler(list):
    def __init__(self):
        self.nodes = set()

    def append(self, error):
        raise error
