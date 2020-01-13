import pytest
from yglu.expression import *
from yglu.tree import *

class Doc:
    root = None

doc = Doc()

def init_doc(root):
    doc.root = root

def test_execution():
    doc.root = {'a': 1}
    assert Expression("$.a + 1", doc).content() == 2


def test_simple_reference():
    m = Mapping()
    s = Sequence()
    m['a'] = Scalar(2)
    m['b'] = Expression('$.a + 1', doc)
    init_doc(m)
    assert m['b'] == 3


def test_sequence_references():
    m = Mapping()
    s = Sequence()
    m['s'] = s
    s.append(Expression('$.s[1] + 1', doc))
    s.append(Scalar(2))
    m['a'] = Expression('$.s[0] + 1', doc)
    init_doc(m)
    assert m['a'] == 4
    assert m == {'s': [3, 2], 'a': 4}


def test_multiple_references():
    m = Mapping()
    s = Sequence()
    m['s'] = s
    s.append(Expression('$.s[1] + 1', doc))
    s.append(Scalar(2))
    m['a'] = Expression('$.s[0] + 1', doc)
    m['b'] = Expression('$["a"] * 2', doc)
    init_doc(m)
    assert m['b'] == 8
    assert m == {'s': [3, 2], 'b': 8, 'a': 4}


def test_circular_reference():
    m = Mapping()
    s = Sequence()
    m['s'] = s
    s.append(Expression('$.s[1]', doc))
    s.append(Expression('$.b', doc))
    m['b'] = Expression('$.s[0]', doc)
    init_doc(m)
    try:
        m['b']
    except CircularReferenceException:
        return
    assert False
