from .utils import assert_like

def test_like():
    input = '''

        hello
        world
                    '''
    assert_like(input, 'hello\nworld')
