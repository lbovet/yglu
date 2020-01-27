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


def test_key_error_shortcut():
    input = 'key1: !? .b\n'
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert('key not found' in message)
        assert('line 1, column 10' in message)


def test_key_error_space():
    input = 'key1: !?   .b\n'
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert('key not found' in message)
        assert('line 1, column 12' in message)


def test_circular_reference():
    input = '''
        a: !? .b
        b: !? .c
        c: !? .a
        '''
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert('circular' in message)
        assert('line 1, column 7' in message)


def test_import_error():
    input = 'a: !? $import("filenotfound")'
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert('No such file' in message)
        assert('line 1, column 7' in message)


def test_null_key():
    input = '!? null: 1'
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert('mapping key is null' in message)
        assert('line 1, column 4' in message)


def test_undefined():
    input = 'a'
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert('document is not a mapping nor a sequence' in message)
        assert('line 1, column 1' in message)


def test_empty_for_loop():
    input = '''
        ? !for '[1,2,3]'
        :
        '''
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert('object is not callable' in message)
        assert('line 1, column 1' in message)


def test_non_scalar_expression():
    input = '''
        a: !?
            asd: 2
        '''
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert('expected a scalar node' in message)
        assert('line 1, column 4' in message)
