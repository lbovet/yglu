from yglu.builder import build


def test_no_tags():
    data = build(
        """
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
        """
    )
    assert data["key2"] == "item2"
    assert data["list"][1] == 2
    assert data["key4"]["key5"] == "item5"
    assert "item6" in data["key4"]["key6"]


def test_invisible():
    data = build(
        """
        a: !- 1
        b: !-
            - 2
            - 3
        c: !-
            x: 4
            y: 5
        d: 6
        """
    )
    assert data["a"] == 1
    assert data == {"d": 6}


def test_simple_expression():
    data = build(
        """
    a: 1
    b: !? $_.a + 1
    c:
        - !- $_.b + 1
        - !? $_.c[0] + 1
    """
    )
    assert data == {"a": 1, "b": 2, "c": [4]}


def test_single_value_doc():
    data = build("1").content()
    assert data == 1


def test_empty_string():
    data = build("")
    assert data is None
