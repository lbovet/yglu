''' Loads YAML with line/column '''
import sys
import ruamel.yaml


class Str(ruamel.yaml.scalarstring.ScalarString):
    __slots__ = ('lc')

    style = ""

    def __new__(cls, value):
        return ruamel.yaml.scalarstring.ScalarString.__new__(cls, value)


class MyPreservedScalarString(ruamel.yaml.scalarstring.PreservedScalarString):
    __slots__ = ('lc')


class MyDoubleQuotedScalarString(ruamel.yaml.scalarstring.DoubleQuotedScalarString):
    __slots__ = ('lc')


class MySingleQuotedScalarString(ruamel.yaml.scalarstring.SingleQuotedScalarString):
    __slots__ = ('lc')


class MyConstructor(ruamel.yaml.constructor.RoundTripConstructor):
    def construct_scalar(self, node):
        # type: (Any) -> Any
        if not isinstance(node, ruamel.yaml.nodes.ScalarNode):
            raise ruamel.yaml.constructor.ConstructorError(
                None, None,
                "expected a scalar node, but found %s" % node.id,
                node.start_mark)

        if node.style == '|' and isinstance(node.value, ruamel.yaml.compat.text_type):
            ret_val = MyPreservedScalarString(node.value)
        elif bool(self._preserve_quotes) and isinstance(node.value, ruamel.yaml.compat.text_type):
            if node.style == "'":
                ret_val = MySingleQuotedScalarString(node.value)
            elif node.style == '"':
                ret_val = MyDoubleQuotedScalarString(node.value)
            else:
                ret_val = Str(node.value)
        else:
            ret_val = Str(node.value)
        ret_val.lc = ruamel.yaml.comments.LineCol()
        ret_val.lc.line = node.start_mark.line
        ret_val.lc.col = node.start_mark.column
        return ret_val


yaml = ruamel.yaml.YAML()
yaml.Constructor = MyConstructor


def add_constructor(tag, constructor):
    MyConstructor.add_constructor(tag, constructor)


def load(source):
    return yaml.load(source)
