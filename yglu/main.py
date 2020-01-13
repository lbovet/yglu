
import os
from .functions import definitions
from .expression import add_context_processor
from .builder import build
from .dumper import dump


for definition in definitions:
    add_context_processor(definition)


def process(input, output, filename=None):
    if filename:
        filename = os.path.abspath(filename)
    dump(build(input, filename), output)

