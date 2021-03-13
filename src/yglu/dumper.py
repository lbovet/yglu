''' Serialization into YAML text '''

import ruamel.yaml
from .loader import SimpleString
from .tree import (Mapping, Sequence, Scalar, NodeException)
from io import StringIO


def dump(tree, output, errors=[]):
    yaml = ruamel.yaml.YAML()

    def represent_mapping(representer, mapping):
        filtered = []
        for (k,v) in mapping.items():
            if v is not None:
                filtered.append((k,v))
        return representer.represent_mapping(u'tag:yaml.org,2002:map', dict(filtered))

    def represent_sequence(representer, sequence):
        return representer.represent_sequence(u'tag:yaml.org,2002:seq', sequence)

    def represent_string(representer, string):
        return representer.represent_scalar(u'tag:yaml.org,2002:str', string)

    def represent_scalar(representer, scalar):
        return representer.represent_data(scalar.content())

    yaml.representer.add_representer(Mapping, represent_mapping)
    yaml.representer.add_representer(Sequence, represent_sequence)
    yaml.representer.add_representer(Scalar, represent_scalar)
    yaml.representer.add_representer(SimpleString, represent_string)

    if tree is not None:
        try:
            out = StringIO()
            yaml.dump(tree, out)
            if len(errors) == 0:
                output.write(out.getvalue())
        except ruamel.yaml.representer.RepresenterError as error:
            errors.append(NodeException(
                tree, "document is not a mapping nor a sequence"))
        except Exception as error:
            errors.append(error)
