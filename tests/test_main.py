from yglu.main import process
from io import StringIO


def test_process_ok():
    input = '''
        a: 1 
        b: 2
    '''
    output = StringIO()
    process(input, output)
    output.flush()
    assert output.getvalue() == 'a: 1\nb: 2\n'


def test_process_failure():
    input = '''
        a: 1 
        b
    '''
    output = StringIO()
    errors = []
    process(input, output, None, errors)
    assert len(errors) == 1
