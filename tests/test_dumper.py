from yglu.dumper import dump
from .utils import *


def test_no_tags():
    input = '''
        key1: '{ '
        key2:
            key3: ho
            key4: 3
        key5:
            - 1
            - hello
        '''
    assert_like(next(process(input)), input)


def test_expression():
    input = '''
        a: 2
        b: !? $_.a + 1
        c: !? "'{' + hello"
        '''
    expected = '''
        a: 2
        b: 3
        c: '{hello'
        '''
    assert_like(next(process(input)), expected)


def test_empty_doc():
    assert list(process('')) == []


def test_doc_separator():
    input = outdent('''
        ---
        ---
        a: 1
        ---
        ---
        ''')
    assert list(process(input)) == ['', 'a: 1\n', '', '']
