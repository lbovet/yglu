import io
import os

from . import loader, main
from .builder import build_all
from .dumper import dump
from .expression import add_context_processor
from .functions import definitions
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


def process_data(input, filename=None):
    """
    Transform data in-memory.

    This implementation is pretty inefficient, not recommended for large data
    structures.
    """
    yaml = loader.create_loader()
    in_str = io.StringIO()
    yaml.dump(input, in_str)
    in_str.seek(0)

    out_str = io.StringIO()
    errs = []
    main.process(in_str, out_str, errors=errs)

    out_str.seek(0)
    return yaml.load(out_str), errs
