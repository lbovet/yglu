""" Loads YAML structure from text input """

import io
import sys

import ruamel.yaml


class String:
    pass


class SimpleString(ruamel.yaml.scalarstring.ScalarString, String):
    __slots__ = "lc"

    style = ""

    def __new__(cls, value):
        return ruamel.yaml.scalarstring.ScalarString.__new__(cls, value)


class PreservedScalarString(ruamel.yaml.scalarstring.PreservedScalarString, String):
    __slots__ = "lc"


class DoubleQuotedScalarString(
    ruamel.yaml.scalarstring.DoubleQuotedScalarString, String
):
    __slots__ = "lc"


class SingleQuotedScalarString(
    ruamel.yaml.scalarstring.SingleQuotedScalarString, String
):
    __slots__ = "lc"


class PositionalContructor(ruamel.yaml.constructor.RoundTripConstructor):
    def construct_scalar(self, node):
        if not isinstance(node, ruamel.yaml.nodes.ScalarNode):
            raise ruamel.yaml.constructor.ConstructorError(
                None,
                None,
                "expected a scalar node, but found %s" % node.id,
                node.start_mark,
            )

        if node.style == "|" and isinstance(node.value, str):
            ret_val = SimpleString(node.value)
        elif bool(self._preserve_quotes) and isinstance(node.value, str):
            if node.style == "'":
                ret_val = SingleQuotedScalarString(node.value)
            elif node.style == '"':
                ret_val = DoubleQuotedScalarString(node.value)
            else:
                ret_val = SimpleString(node.value)
        else:
            ret_val = SimpleString(node.value)
        ret_val.lc = ruamel.yaml.comments.LineCol()
        ret_val.lc.line = node.start_mark.line
        ret_val.lc.col = node.start_mark.column
        return ret_val


def create_loader():
    yaml = ruamel.yaml.YAML()
    yaml.Constructor = PositionalContructor
    yaml.allow_duplicate_keys = True
    return yaml


def add_constructor(tag, constructor):
    PositionalContructor.add_constructor(tag, constructor)


def load_all(source, errors=[]):
    if source == sys.stdin:
        buffer = io.StringIO()
        try:
            for line in source:
                if line.replace(" ", "").startswith("---"):
                    yield create_loader().load(buffer.getvalue())
                    buffer = io.StringIO()
                else:
                    buffer.writelines(line)

            yield create_loader().load(buffer.getvalue())
        except Exception as error:
            errors.append(error)
    else:
        try:
            for doc in create_loader().load_all(source):
                yield doc
        except Exception as error:
            errors.append(error)


def load(source):
    return create_loader().load(source)
