import os
import sys
from .functions import definitions
from .expression import add_context_processor
from .builder import build_all
from .dumper import dump
from .tree import NodeException


for definition in definitions:
    add_context_processor(definition)

class ErrorList(list):
    def __init__(self):
        self.nodes = set()
    def append(self, error):
        if not isinstance(error, NodeException) or error.node not in self.nodes:
            super().append(error)
        if isinstance(error, NodeException):
            self.nodes.add(error.node)

def process(input, output, filename=None, errors=[]):
    if filename:
        filename = os.path.abspath(filename)
    first = True

    for doc in build_all(input, filename, errors):
        if not first:
            output.write("---\n")
        else:
            first = False
        dump(doc, output, errors)
