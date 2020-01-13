''' Transforms the parsed YAML structure into a tree '''

from . import loader
from .tree import (Scalar, Sequence, Mapping)
from .expression import (Expression, Function, FunctionBlock, enter_scope)
from ruamel.yaml.nodes import (ScalarNode, SequenceNode, MappingNode)
from ruamel.yaml.comments import TaggedScalar


def build(source):
    result = convert(loader.load(source))
    enter_scope(result)
    return result


def convert(node):
    if isinstance(node, dict):
        return Mapping([(k, convert(v)) for (k, v) in node.items()])
    if isinstance(node, list):
        return Sequence([convert(v) for v in node])
    if isinstance(node, TaggedNode):
        return node.create()
    return Scalar(node)


def construct_node(self, node):
    if isinstance(node, ScalarNode):
        return self.construct_scalar(node)
    if isinstance(node, MappingNode):
        return [c for c in self.construct_yaml_map(node)][0]
    if isinstance(node, SequenceNode):
        return self.construct_sequence(node)


class TaggedNode:
    def __init__(self, value):
        self.value = value


class InvisibleNode(TaggedNode):
    def create(self):
        if isinstance(self.value, str):
            result = Expression(self.value)
        else:
            result = convert(self.value)
        result.visible = False
        return result


def invisible_constructor(self, node):
    return InvisibleNode(construct_node(self, node))


loader.add_constructor('!-', invisible_constructor)


class ExpressionNode(TaggedNode):
    def create(self):
        result = Expression(self.value)
        return result


def expression_constructor(self, node):
    if isinstance(node, ScalarNode):
        return ExpressionNode(self.construct_scalar(node))
    assert False, 'Expression nodes must be scalar'


loader.add_constructor('!?', expression_constructor)


class FunctionNode(TaggedNode):
    def create(self):
        result = Function(self.value)
        return result


class FunctionBlockNode(TaggedNode):
    def __init__(self, value, constructor):
        self.value = value
        self.constructor = constructor
    def create(self):
        result = FunctionBlock(self, lambda node: convert(construct_node(self.constructor, node)))
        return result


def function_constructor(self, node):
    if isinstance(node, ScalarNode):
        return FunctionNode(self.construct_scalar(node))
    else:
        return FunctionBlockNode(node, self)


loader.add_constructor('!()', function_constructor)
