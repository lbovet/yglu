''' Transforms the parsed YAML structure into a tree '''

from . import loader
from .tree import (Document, Scalar, Sequence, Mapping)
from .expression import (Expression, Function, FunctionBlock)
from ruamel.yaml.nodes import (ScalarNode, SequenceNode, MappingNode)
from ruamel.yaml.comments import TaggedScalar


def build(source, filepath=None):
    result = []
    for yamlDoc in loader.load(source):
        doc = Document()
        tree = convert(yamlDoc, doc)
        doc.filepath = filepath
        doc.root = tree
        result.append(tree)
    return result

def convert(node, doc):
    if isinstance(node, dict):
        return Mapping([(k, convert(v, doc)) for (k, v) in node.items()], doc)
    if isinstance(node, list):
        return Sequence([convert(v, doc) for v in node], doc)
    if isinstance(node, TaggedNode):
        return node.create(doc)
    return Scalar(node, doc)


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
    def create(self, doc):
        if isinstance(self.value, str):
            result = Expression(self.value, doc)
        else:
            result = convert(self.value, doc)
        result.visible = False
        return result


def invisible_constructor(self, node):
    return InvisibleNode(construct_node(self, node))


loader.add_constructor('!-', invisible_constructor)


class ExpressionNode(TaggedNode):
    def create(self, doc):
        result = Expression(self.value, doc)
        return result


def expression_constructor(self, node):
    if isinstance(node, ScalarNode):
        return ExpressionNode(self.construct_scalar(node))
    assert False, 'Expression nodes must be scalar'


loader.add_constructor('!?', expression_constructor)


class FunctionNode(TaggedNode):
    def create(self, doc):
        result = Function(self.value, doc)
        return result


class FunctionBlockNode(TaggedNode):
    def __init__(self, value, constructor):
        self.value = value
        self.constructor = constructor

    def create(self, doc):
        result = FunctionBlock(self, lambda node: convert(
            construct_node(self.constructor, node), doc))
        return result


def function_constructor(self, node):
    if isinstance(node, ScalarNode):
        return FunctionNode(self.construct_scalar(node))
    else:
        return FunctionBlockNode(node, self)


loader.add_constructor('!()', function_constructor)
