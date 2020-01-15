
import os
from .functions import definitions
from .expression import add_context_processor
from .builder import build_all
from .dumper import dump


for definition in definitions:
    add_context_processor(definition)


def process(input, output, filename=None):
    if filename:
        filename = os.path.abspath(filename)    
    first = True
    for doc in build_all(input, filename):
        if not first:
            output.write("---\n")
        else:
            first = False
        dump(doc, output)
