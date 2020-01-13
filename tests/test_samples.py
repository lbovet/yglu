import os
import glob
from yglu.dumper import dump
from .test_utils import *


path = os.path.dirname(os.path.realpath(__file__))
filenames = [f for f in glob.glob(path + "/samples/**/*.yml", recursive=True)]


def test_samples():
    os.environ['YGLU_ENABLE_ENV'] = 'true'
    for filename in filenames:
        print("Sample: "+filename)
        with open(filename) as file:
            docs = file.read().split("---\n")
            input = process(docs[0])
            output = process(docs[1])
            assert_like(input, output)
