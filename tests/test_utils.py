from yglu.dumper import dump
from yglu.builder import build
from yglu.expression import add_context_processor
from yglu.functions import definitions
import io

for definition in definitions:
    add_context_processor(definition)

def process(input, filepath=None):
    result = []
    for doc in build(input, filepath):
        stream = io.StringIO()
        dump(doc, stream)
        result.append(stream.getvalue())
    return result

def assert_like(d1, d2):
    assert outdent(d1) == outdent(d2)


def test_like():
    input = '''

        hello
        world
                    '''
    assert_like(input, 'hello\nworld')


def outdent(doc):
    offset = 0
    for c in doc:
        if c == ' ':
            offset += 1
        elif c == '\n':
            offset = 0
        else:
            break
    result = []
    for line in doc.splitlines():
        if len(line) >= offset:
            line = line[offset:]
        line = line.strip()
        if len(line) > 0:
            result.append(line)
    return '\n'.join(result)
