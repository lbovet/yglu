""" Command-line interface """

import sys

from . import __version__
from .main import process
from .tree import NodeException


class ErrorList(list):
    def __init__(self):
        self.nodes = set()

    def append(self, error):
        if not isinstance(error, NodeException) or error.node not in self.nodes:
            super().append(error)
            sys.stderr.write(str(error) + "\n")
            sys.stderr.flush()
        if isinstance(error, NodeException):
            self.nodes.add(error.node)


def main():
    errors = ErrorList()
    if len(sys.argv) > 1:
        if sys.argv[1] == "-v":
            print("yglu " + __version__)
            sys.exit(0)
        if sys.argv[1].startswith("-"):
            print("Usage: yglu [options] [<filename>]")
            print()
            print("Options:")
            print("  -v - -version          Print version and exit.")
            print("  -h - -help             Print help and exit.")
            sys.exit(0)
        try:
            filename = sys.argv[1]
            with open(filename) as file:
                process(file, sys.stdout, filename, errors)
        except FileNotFoundError:
            sys.stderr.write("File not found: " + sys.argv[1] + "\n")
            sys.exit(1)
    else:
        process(sys.stdin, sys.stdout, None, errors)
    if len(errors) > 0:
        sys.stderr.write("Finished with errors.\n")
        sys.exit(1)
