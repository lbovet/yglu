from .utils import assert_like, outdent


def test_like():
    input = """

        hello
        world
                    """
    assert_like(input, "hello\nworld")


def test_outdent():
    input = """
        a:
            b: 2
        """
    assert outdent(input) == "a:\n    b: 2"
