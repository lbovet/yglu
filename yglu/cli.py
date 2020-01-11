''' Command-line interface '''

import sys
from . import version
from .builder import build
from .dumper import dump


def process(input):
    dump(build(input), sys.stdout)


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '-v':
            print('yglu '+version)
            sys.exit(0)
        if sys.argv[1].startswith('-'):
            print('Usage: yglu [options] [<filename>]')
            print()
            print('Options:')
            print('  -v - -version          Print version and exit.')
            print('  -h - -help             Print help and exit.')
            sys.exit(0)
        try:
            with open(sys.argv[1]) as file:
                process(file)
        except FileNotFoundError:
            sys.stderr.write('File not found: '+sys.argv[1]+'\n')
            sys.exit(1)
    else:
        process(sys.stdin.read())
