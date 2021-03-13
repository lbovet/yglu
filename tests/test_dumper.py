from .utils import assert_like, outdent, process, process_all


def test_no_tags():
    input = """
        key1: '{ '
        key2:
          key3: ho
          key4: 3
        key5:
        - 1
        - hello
        """
    assert_like(process(input), input)


def test_expression():
    input = """
        a: 2
        b: !? $_.a + 1
        c: !? "'{' + hello"
        """
    expected = """
        a: 2
        b: 3
        c: '{hello'
        """
    assert_like(process(input), expected)


def test_empty_doc():
    assert list(process_all("")) == []


def test_doc_separator():
    input = outdent(
        """
        ---
        ---
        a: 1
        ---
        b: 2
        ---
        """
    )
    assert list(process_all(input)) == ["", "a: 1\n", "b: 2\n", ""]


def test_null():
    input = """
        a: 1
        b: null
        c: !? null
        """
    expected = """
        a: 1
        """
    assert_like(process(input), expected)


def test_scalar():
    input = """
        2
        """
    expected = """2
...
"""
    assert_like(process(input), expected)


def test_expression_in_key():
    input = """
        a: b
        !? .a: 1
        """
    expected = """
        a: b
        b: 1
        """
    assert_like(process(input), expected)


def test_mapping_in_sequence():
    input = """
        a: !-
          - b: 1
            c: 2
        d: !? ($_.a)
        """
    expected = """
        d:
        - b: 1
          c: 2
        """
    assert_like(process(input), expected)


def test_sequence_in_function():
    input = """
        a: !()
          - b: 1
            c: 2
        d: !? ($_.a)(1)
        """
    expected = """
        d:
        - b: 1
          c: 2
        """
    assert_like(process(input), expected)


def test_sequence_loop():
    input = """
        a: !-
          - 1
          - 3
        b:
          - ? !for .a
            : !()
              - x: !? $
                y: !? $ + 1
        """
    expected = """
        b:
        - x: 1
          y: 2
        - x: 3
          y: 4
        """
    assert_like(process(input), expected)


def test_if_override():
    input = """
        t: !-
            a: 1
            b: 2
        u: !-
            a: !? null
        v:
            !if true: !? .t
            !if true: !? .u
        """
    expected = """
        v:
          b: 2
        """
    assert_like(process(input), expected)


def test_this():
    input = """
        a: !()
            b: !- 2
            c: !? $ + $this.b
        d: !? ($_.a)(2)
        """
    expected = """
        d:
          c: 4
        """
    assert_like(process(input), expected)


def test_apply():
    input = """
        a: !()
            b: !? $.x + 1
            c: !? $.y + 2
        d:
            !apply .a:
                x: 1
                y: 2
        """
    expected = """
        d:
          b: 2
          c: 4
        """
    assert_like(process(input), expected)


def test_apply_in_array():
    input = """
        a: !()
            b: !? $.x + 1
            c: !? $.y + 2
        d:
            - !apply .a:
                x: 1
                y: 2
        """
    expected = """
        d:
        - b: 2
          c: 4
        """
    assert_like(process(input), expected)
