''' Serialization into YAML text '''

import ruamel.yaml
from .loader import SimpleString
from .tree import (Mapping, Sequence, Scalar)


def dump(tree, output, errors=[]):
    yaml = ruamel.yaml.YAML()

    def represent_mapping(representer, mapping):
        return representer.represent_mapping(u'tag:yaml.org,2002:map', mapping)

    def represent_sequence(representer, sequence):
        return representer.represent_sequence(u'tag:yaml.org,2002:seq', sequence)

    def represent_string(representer, string):
        return representer.represent_scalar(u'tag:yaml.org,2002:str', string)

    yaml.representer.add_representer(Mapping, represent_mapping)
    yaml.representer.add_representer(Sequence, represent_sequence)
    yaml.representer.add_representer(SimpleString, represent_string)
   
    if tree is not None:
        try:
            yaml.dump(tree, output)
        except Exception as error:
            errors.append(error)
