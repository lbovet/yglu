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


class Expression(Node):
    def __init__(self, expression, doc):        
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
        result = engine(self.expression).evaluate(context=context)
        pop_stack()
        return result


class Function(Node):
    def __init__(self, expression, doc):
        self.expression = expression
        self.doc = doc
        self.visible = False

    def eval(self, scope):
        context = get_context(self.doc.root).create_child_context()
        context['$'] = scope
        result = engine(self.expression).evaluate(context=context)
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
