from yglu.tree import Mapping, MergeKey, Node, Scalar, Sequence


def test_constant():
    m = Mapping()
    m["a"] = Scalar(1)
    assert m["a"] == 1
    s = Sequence()
    s.append(Scalar("hello"))
    assert s[0] == "hello"


def test_constructor():
    m = Mapping({Scalar("a"): Scalar(2)})
    assert m["a"] == 2
    s = Sequence([Scalar(1), Scalar(2)])
    assert s[1] == 2


def test_sequence_accessors():
    s = Sequence()
    s.append(Scalar(1))
    hidden = Scalar(3)
    hidden.visible = False
    s.append(hidden)
    s.append(Scalar(2))
    assert [i for i in s] == [1, 2]
    assert s == [1, 2]
    assert s[1] == 3


def test_mapping_accessors():
    m = Mapping()
    m["a"] = Scalar(1)
    hidden = Scalar(3)
    hidden.visible = False
    m["X"] = hidden
    m["b"] = Scalar(2)
    assert [i for i in m.items()] == [("a", 1), ("b", 2)]
    assert m == {"a": 1, "b": 2}
    assert m["X"] == 3


def test_content():
    class OneNode(Node):
        def __init__(self):
            Node.__init__(self, None)

        version = 0

        def create_content(self):
            self.version += 1
            return self.version

    n = OneNode()
    s = Sequence()
    s.append(n)
    s.append(n)
    m2 = Mapping()
    m2["s"] = s
    m = Mapping()
    m["s"] = s
    m["n"] = n
    m["m2"] = m2

    assert m["s"][0] == 1
    assert m["s"][1] == 1
    assert m["n"] == 1
    assert m["m2"]["s"] == [1, 1]


def test_merge_mapping():
    class TestNode(MergeKey):
        def __init__(self):
            Node.__init__(self, None)

        def entries(self, value):
            return value

    sub = Mapping()
    sub["b"] = Scalar(2)
    sub["c"] = Scalar(3)
    m = Mapping({Scalar("a"): Scalar(1), TestNode(): sub})

    assert m == {"a": 1, "b": 2, "c": 3}


def test_merge_sequence():
    class TestNode(MergeKey):
        def __init__(self):
            Node.__init__(self, None)

        def entries(self, value):
            return value

    sub = Sequence([Scalar(1), Scalar(2)])
    Sequence([Scalar(0), Mapping({TestNode(): sub}), Scalar(3)])

    # TODO: implement later
    # assert s == [0, 1, 2, 3]
