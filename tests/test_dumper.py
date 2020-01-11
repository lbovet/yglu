from yglu.dumper import dump
from .test_utils import *

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
    output = process(input)
    assert_like(input, output)

def test_expression():
    input = '''
        a: 2
        b: !? $.a + 1
        c: !? "'{' + hello"
        '''    
    expected = '''
        a: 2
        b: 3
        c: '{hello'
        '''
    assert_like(process(input), expected)