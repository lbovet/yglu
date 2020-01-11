import pytest
from yglu.builder import build
from yglu.expression import init_scope
import ruamel.yaml


def test_no_tags():
    data = build('''
        key1: 1
        list:
            - 1
            - 2
        key2: item2
        key3: item3        
        key4: 
            key5: 'item5'
            key6: |
                item6
        ''')
    assert data['key2'] == 'item2'
    assert data['list'][1] == 2
    assert data['key4']['key5'] == 'item5'


def test_invisible():
    data = build('''
        a: !- 1
        b: !-
            - 2
            - 3
        c: !-
            x: 4
            y: 5
        d: 6
        ''')
    assert data['a'] == 1
    assert data == {'d': 6}


def test_simple_expression():
    data = build('''
    a: 1
    b: !? $.a + 1 
    c:
        - !- $.b + 1
        - !? $.c[0] + 1
    ''')

    assert data == {'a': 1, 'b': 2, 'c': [4]}
