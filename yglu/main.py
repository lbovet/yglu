
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
    docs = build(input, filename)
    i = 0
    for doc in docs:
        dump(doc, output)
        i+=1
        if i < len(docs):
            output.write("---\n")
