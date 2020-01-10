from yglu.tree import *


def test_constant():
    m = Mapping()
    m['a'] = Scalar(1)
    assert m['a'] == 1
    s = Sequence()
    s.append(Scalar('hello'))
    assert s[0] == 'hello'


def test_sequence_accessors():
    s = Sequence()
    s.append(Scalar(1))
    hidden = Scalar(3)
    hidden.visible = False
    s.append(hidden)
    s.append(Scalar(2))
    assert [i for i in s] == [1, 2]
    assert s == [1, 2]
    assert str(s) == '[1, 2]'
    assert s[1] == 3

def test_mapping_accessors():
    m = Mapping()
    m['a'] = Scalar(1)
    hidden = Scalar(3)
    hidden.visible = False
    m['X'] = hidden
    m['b'] = Scalar(2)
    assert m.items() == [('a', 1), ('b', 2)]
    assert m == { 'a': 1, 'b': 2 }
    assert str(m) == "{'a': 1, 'b': 2}"
    assert m['X'] == 3

def test_content():
    class OneNode(Node):
        version = 0
        def create_content(self):
            self.version += 1
            return self.version

    n = OneNode()
    s = Sequence()
    s.append(n)
    s.append(n)
    m2 = Mapping()
    m2['s'] = s
    m = Mapping()
    m['s'] = s
    m['n'] = n
    m['m2'] = m2

    assert m['s'][0] == 1
    assert m['s'][1] == 1
    assert m['n'] == 1
    assert m['m2']['s'] == [1, 1]
