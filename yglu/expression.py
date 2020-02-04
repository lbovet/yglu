''' Evaluation of YAQL expressions '''

import os
import yaql
from ruamel.yaml.nodes import (MappingNode, SequenceNode)
from .tree import (Node, Mark, NodeException)

engine = yaql.factory.YaqlFactory(allow_delegates=True).create(options={
    'yaql.convertInputData': False,
})
scopes = []
stack = []
contexts = {}
context_processors = []


def add_context_processor(processor):
    context_processors.append(processor)


def get_context(root):
    key = id(root)
    if key in contexts:
        context = contexts[key]
    else:
        context = yaql.create_context(delegates=True)
        if 'YGLU_ENABLE_ENV' in os.environ:
            context['$env'] = os.environ
        context['$_'] = root
        for process in context_processors:
            process(context, root)
        contexts[key] = context
    return context


def push_stack(node):
    if node in stack:
        raise CircularReferenceException(node, stack)
    stack.append(node)


def pop_stack():
    stack.pop()

class Scope:
    def __init__(self, arg, this):
        self.arg = arg
        self.this = this

def push_scope(scope):
    scopes.append(scope)


def pop_scope():
    scopes.pop()


class Mark:
    def __init__(self, line, column):
        self.line = line
        self.column = column


class ExpressionException(NodeException):
    def __init__(self, node, cause):
        self.node = node
        self.cause = cause


def evaluate(node, context):
    try:
        return engine(node.expression).evaluate(context=context)
    except ExpressionException as e:
        if node.doc.errors is None:            
            raise e
    except Exception as e:
        error = ExpressionException(node, e)
        if node.doc.errors is not None:
            node.doc.errors.append(error)
            if len(stack) > 1:
                raise Exception("error in referenced node")
        else:
            raise error

class Holder:
    def __init__(self, value):
        self.value = value


class Expression(Node):
    def __init__(self, expression, doc, source=None):
        Node.__init__(self, doc, source)
        if expression.startswith('.'):
            self.expression = '$_'+expression
        else:
            self.expression = expression
        self.doc = doc

    def create_content(self):
        push_stack(self)
        context = get_context(self.doc.root).create_child_context()
        if len(scopes) > 0:
            context['$'] = scopes[-1].arg
            context['$this'] = scopes[-1].this
        try:
            result = evaluate(self, context)
        finally:
            pop_stack()
        if isinstance(result, Holder):
            return result.value
        else:
            return result


class Function(Node):
    def __init__(self, expression, doc, source):
        Node.__init__(self, doc, source)
        self.expression = expression
        self.visible = False

    def eval(self, arg=None):
        context = get_context(self.doc.root).create_child_context()
        context['$'] = arg
        result = evaluate(self, context)
        return result

    def create_content(self):
        return self.eval


class FunctionBlock(Node):
    def __init__(self, constructor):
        Node.__init__(self, None)
        self.visible = False
        self.constructor = constructor

    def eval(self, arg):
        node = self.constructor()
        push_scope(Scope(arg, node))
        if isinstance(node, Node):
            node.receive(lambda x: x)  # force content creation
        if isinstance(node, dict):
            result = dict(node.items())
        else:
            result = list(node)
        pop_scope()
        return result

    def create_content(self):
        return self.eval


class CircularReferenceException(ExpressionException):
    def __init__(self, node, stack):
        super().__init__(node, "circular reference in expression")
        self.stack = stack
