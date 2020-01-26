from yglu.dumper import dump
from .utils import *


def test_empty_expression():
    input = 'key1: !?'
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert('unexpected end of statement' in message)
        assert('line 1, column 9' in message)


def test_parse_error():
    input = 'key1: !? 12.'
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert('unexpected end of statement' in message)
        assert('line 1, column 10' in message)



def test_lexical_error():
    input = 'key1: !? $_^.bla\n'
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert('illegal character' in message)
        assert('line 1, column 12' in message)


def test_key_error():
    input = 'key1: !? $_.b\n'
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert('key not found' in message)
        assert('line 1, column 10' in message)
