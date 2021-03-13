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

<<<<<<< Updated upstream
def process(input, output, filename=None, errors=[]):
=======
def process(input, output, error_stream, errors, filename=None):
>>>>>>> Stashed changes
    if filename:
        filename = os.path.abspath(filename)
    first = True
<<<<<<< Updated upstream

    for doc in build_all(input, filename, errors):
=======
    success = True
    for doc in build_all(input, filename):
>>>>>>> Stashed changes
        if not first:
            output.write("---\n")
        else:
            first = False
<<<<<<< Updated upstream
        dump(doc, output, errors)

def process_data(input, filename=None):
    """
    Transform data in-memory.

    This implementation is pretty inefficient, not recommended for large data structures.
    """
    yaml = loader.create_loader()
    in_str = io.StringIO()
    yaml.dump(input, in_str)
    in_str.seek(0)

    out_str = io.StringIO()
    errs= []
    main.process(in_str, out_str, errors=errs)

    out_str.seek(0)
    return yaml.load(out_str), errs
=======
        try:
            dump(doc, output)
        except Exception as e:
            error_stream.write(str(e)+"\n")
            errors.append(e)
    if not success:
        sys.stderr.write("There were errors.\n")
>>>>>>> Stashed changes
