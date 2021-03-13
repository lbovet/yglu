import os

from .utils import process

os.environ["YGLU_IMPORT_ALLOW"] = "/tmp/yglu1:/tmp/yglu2"


def test_illegal_relative_import():
    input = """
        key1: !? $import('../test.yml')
        """
    try:
        process(input)
        assert False
    except Exception as e:
        assert "YGLU_IMPORT_ALLOW" in str(e)


def test_illegal_absolute_import():
    input = """
        key1: !? $import('/var/test.yml')
        """
    try:
        process(input)
        assert False
    except Exception as e:
        assert "YGLU_IMPORT_ALLOW" in str(e)


def test_legal_absolute_import():
    input = """
        key1: !? $import('/tmp/yglu2/test.yml')
        """
    try:
        process(input)
        assert False
    except Exception as e:
        assert type(e.cause) == FileNotFoundError
