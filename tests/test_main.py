from io import StringIO

from yglu.main import process

from .utils import outdent


def test_process_ok():
    input = """
        a: 1
        b: 2
        ---
        c: 3
    """
    output = StringIO()
    process(outdent(input), output)
    assert output.getvalue() == "a: 1\nb: 2\n---\nc: 3\n"


def test_process_failure():
    input = """
        a: 1
        b
    """
    output = StringIO()
    errors = []
    process(input, output, None, errors)
    assert len(errors) == 1
