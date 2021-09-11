""" Transforms the parsed YAML structure into a tree """

from ruamel.yaml.constructor import ConstructorError
from ruamel.yaml.nodes import MappingNode, ScalarNode, SequenceNode

from . import loader
from .expression import Expression, Function, FunctionBlock
from .tree import Document, Mapping, MergeKey, NodeException, Scalar, Sequence


def build(source, filepath=None, errors=None):
    yaml_doc = loader.load(source)
    return create_tree(yaml_doc, filepath, errors)


def build_all(source, filepath=None, errors=[]):
    for yaml_doc in loader.load_all(source, errors):
        yield create_tree(yaml_doc, filepath, errors)


def create_tree(yaml_doc, filepath, errors=None):
    if yaml_doc is None:
        return None
    doc = Document()
    tree = convert(yaml_doc, doc)
    doc.filepath = filepath
    doc.root = tree
    doc.errors = errors
    return tree


def convert(node, doc):
    if isinstance(node, dict):
        return Mapping(
            [(convert(k, doc), convert(v, doc)) for (k, v) in node.items()], doc
        )
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
        result = [c for c in self.construct_yaml_seq(node)][0]
        return result


class TaggedNode:
    def __init__(self, value, source=None):
        self.value = value
        self.source = source


class InvisibleNode(TaggedNode):
    def create(self, doc):
        if isinstance(self.value, str):
            result = Expression(self.value, doc, self.source)
        else:
            result = convert(self.value, doc)
        result.visible = False
        return result


def invisible_constructor(self, node):
    return InvisibleNode(construct_node(self, node), node)


loader.add_constructor("!-", invisible_constructor)


class ExpressionNode(TaggedNode):
    def create(self, doc):
        result = Expression(self.value, doc, self.source)
        return result


def expression_constructor(self, node):
    if isinstance(node, ScalarNode):
        return ExpressionNode(self.construct_scalar(node), node)
    else:
        raise ConstructorError(
            None,
            None,
            "expected a scalar node, but found %s" % node.id,
            node.start_mark,
        )


loader.add_constructor("!?", expression_constructor)


class FunctionNode(TaggedNode):
    def create(self, doc):
        result = Function(self.value, doc, self.source)
        return result


class FunctionBlockNode(TaggedNode):
    def __init__(self, value, constructor):
        self.value = value
        self.constructor = constructor
        self.node = construct_node(self.constructor, self.value)

    def create(self, doc):
        result = FunctionBlock(lambda: convert(self.node, doc))
        return result


def function_constructor(self, node):
    if isinstance(node, ScalarNode):
        return FunctionNode(self.construct_scalar(node))
    else:
        return FunctionBlockNode(node, self)


loader.add_constructor("!()", function_constructor)


class IfNode(TaggedNode, MergeKey):
    def __init__(self, doc, node):
        TaggedNode.__init__(self, doc, node)
        MergeKey.__init__(self)

    def create(self, doc):
        self.expression = Expression(self.value, doc, self.source)
        return self

    def merge(self, parent, source):
        if self.expression.content():
            MergeKey.merge(self, parent, source)


def if_constructor(self, node):
    if isinstance(node, ScalarNode):
        return IfNode(self.construct_scalar(node), node)
    assert False, "expression nodes must be scalar"


loader.add_constructor("!if", if_constructor)


class ForNode(TaggedNode, MergeKey):
    def __init__(self, doc, node):
        TaggedNode.__init__(self, doc, node)
        MergeKey.__init__(self)

    def create(self, doc):
        self.expression = Expression(self.value, doc, self.source)
        return self

    def merge(self, parent, source):
        try:
            for item in self.expression.content():
                MergeKey.merge(self, parent, source.content()(item))
        except Exception as e:
            raise NodeException(self.expression, e)


def for_constructor(self, node):
    if isinstance(node, ScalarNode):
        return ForNode(self.construct_scalar(node), node)
    assert False, "expression nodes must be scalar"


loader.add_constructor("!for", for_constructor)


class ApplyNode(TaggedNode, MergeKey):
    def __init__(self, doc, node):
        TaggedNode.__init__(self, doc, node)
        MergeKey.__init__(self)

    def create(self, doc):
        self.expression = Expression(self.value, doc, self.source)
        return self

    def merge(self, parent, source):
        MergeKey.merge(self, parent, self.expression.content()(source))


def apply_constructor(self, node):
    if isinstance(node, ScalarNode):
        return ApplyNode(self.construct_scalar(node), node)
    assert False, "expression nodes must be scalar"


loader.add_constructor("!apply", apply_constructor)
