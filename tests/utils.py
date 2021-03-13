import io

from yglu.builder import build, build_all
from yglu.dumper import dump
from yglu.expression import add_context_processor
from yglu.functions import definitions

for definition in definitions:
    add_context_processor(definition)


class ErrorHandler(list):
    def append(self, error):
        raise error


def process(input, filepath=None):
    if isinstance(input, str):
        input = outdent(input)
    error_handler = ErrorHandler()
    stream = io.StringIO()
    dump(build(input, filepath), stream, error_handler)
    return stream.getvalue()


def process_all(input, filepath=None, error_handler=[]):
    for doc in build_all(input, filepath, error_handler):
        stream = io.StringIO()
        dump(doc, stream, error_handler)
        yield stream.getvalue()


def assert_like(d1, d2):
    assert outdent(d1) == outdent(d2)


def outdent(doc):
    offset = 0
    for c in doc:
        if c == " ":
            offset += 1
        elif c == "\n":
            offset = 0
        else:
            break
    result = []
    for line in doc.splitlines():
        if len(line) >= offset:
            line = line[offset:]
        line = line.rstrip()
        if len(line) > 0:
            result.append(line)
    return "\n".join(result)
