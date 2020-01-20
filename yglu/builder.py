''' Transforms the parsed YAML structure into a tree '''

from . import loader
from .tree import (Document, Scalar, Sequence, Mapping, MergeKey)
from .expression import (Expression, Function, FunctionBlock)
from ruamel.yaml.nodes import (ScalarNode, SequenceNode, MappingNode)
from ruamel.yaml.comments import TaggedScalar


def build(source, filepath=None):
    yaml_doc = loader.load(source)
    return create_tree(yaml_doc, filepath)


def build_all(source, filepath=None, errors=[]):
    for yaml_doc in loader.load_all(source, errors):
        yield create_tree(yaml_doc, filepath)


def create_tree(yaml_doc, filepath):
    if yaml_doc is None:
        return None
    doc = Document()
    tree = convert(yaml_doc, doc)
    doc.filepath = filepath
    doc.root = tree
    return tree


def convert(node, doc):
    if isinstance(node, dict):
        return Mapping([(convert(k, doc), convert(v, doc)) for (k, v) in node.items()], doc)
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
    assert False, 'expression nodes must be scalar'


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


class IfNode(TaggedNode, MergeKey):
    def create(self, doc):
        self.expression = Expression(self.value, doc)
        return self

    def merge(self, parent, source):
        if self.expression.content():
            MergeKey.merge(self, parent, source)


def if_constructor(self, node):
    if isinstance(node, ScalarNode):
        return IfNode(self.construct_scalar(node))
    assert False, 'expression nodes must be scalar'


loader.add_constructor('!if', if_constructor)


