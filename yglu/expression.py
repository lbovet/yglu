''' Evaluation of YAQL expressions '''

import yaql
from .tree import Node
from ruamel.yaml.nodes import (MappingNode, SequenceNode)

engine = yaql.factory.YaqlFactory(allow_delegates=True).create(options={
    'yaql.convertInputData': False,
})
scopes = []
stack = []
contexts = []


def enter_scope(scope):
    global scopes
    global stack
    scopes.append(scope)
    context = yaql.create_context(delegates=True)
    context['$_'] = scope
    contexts.append(context)
    stack = []

def leave_scope():
    scopes.pop()
    contexts.pop()

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


class Expression(Node):
    def __init__(self, expression):
        self.expression = expression

    def create_content(self):
        push_stack(self)
        result = engine(self.expression).evaluate(data=scopes[-1], context=contexts[-1])
        pop_stack()
        return result


class Function(Node):
    def __init__(self, expression):
        self.expression = expression
        self.visible = False

    def eval(self, scope):
        result = engine(self.expression).evaluate(data=scope, context=contexts[-1])
        return result

    def create_content(self):
        return self.eval


class FunctionBlock(Node):
    def __init__(self, node, constructor):
        self.node = node.value
        self.visible = False
        self.constructor = constructor

    def eval(self, scope):
        push_scope(scope)
        result = dict(self.constructor(self.node).items())
        pop_scope()
        return result

    def create_content(self):
        return self.eval


class CircularReferenceException(Exception):
    pass
