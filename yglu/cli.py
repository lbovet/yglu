import sys
from yglu.builder import build
from yglu.dumper import dump

def process(input):
    dump(build(input), sys.stdout)

def main()
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as file:
            process(file)
    else:
        process(sys.stdin.read())
