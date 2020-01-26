''' Evaluation of YAQL expressions '''

import os
import yaql
from ruamel.yaml.nodes import (MappingNode, SequenceNode)
from .tree import Node

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
        raise CircularReferenceException()
    stack.append(node)


def pop_stack():
    stack.pop()


def push_scope(scope):
    scopes.append(scope)


def pop_scope():
    scopes.pop()

class Mark:
    def __init__(self, line, column):
        self.line = line
        self.column = column

class ExpressionException(Exception):
    def __init__(self, node, cause):
        self.node = node
        self.cause = cause

    def __str__(self):
        filepath = self.node.doc.filepath
        if filepath is None:
            filepath = '<stdin>'
        start_mark = self.start_mark()
        line = start_mark.line
        column = start_mark.column

        if isinstance(self.cause, KeyError):
            message = 'key not found: '+str(self.cause)
        else:
            message = str(self.cause)

        result = message+'\n in "'+filepath + \
            '", line ' + str(start_mark.line+1) + \
            ', column ' + str(start_mark.column+1) + \
            ':\n  '+str(self.node.expression)
        return result

    def start_mark(self):
        column = self.node.source.end_mark.column - len(self.node.expression)
        if hasattr(self.cause, 'position') and self.cause.position:
            column += self.cause.position
        return Mark(self.node.source.start_mark.line, column)

    def end_mark(self):
        return self.node.source.end_mark


def evaluate(node, context):
    try:
        return engine(node.expression).evaluate(context=context)
    except ExpressionException as e:
        raise e
    except Exception as e:
        raise ExpressionException(node, e)


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
            context['$'] = scopes[-1]
        result = evaluate(self, context)
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

    def eval(self, scope=None):
        context = get_context(self.doc.root).create_child_context()
        context['$'] = scope
        result = evaluate(self, context)
        return result

    def create_content(self):
        return self.eval


class FunctionBlock(Node):
    def __init__(self, constructor):
        Node.__init__(self, None)
        self.visible = False
        self.constructor = constructor

    def eval(self, scope):
        push_scope(scope)
        node = self.constructor()
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


class CircularReferenceException(Exception):
    def __init__(self):
        super().__init__("circular reference in expression")
