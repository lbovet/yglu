''' Node containing a YAQL expression to evaluate as content'''
import yaql
from .tree import Node

engine = yaql.factory.YaqlFactory().create(options={
    'yaql.convertInputData': False
})
scope = {}
stack = []


def init(new_scope):
    global scope
    global stack
    scope = new_scope
    stack = []


class ExpressionNode(Node):
    def __init__(self, expression):
        self.expression = expression

    def create_content(self):
        if self in stack:
            raise CircularReferenceException()
        stack.append(self)
        result = engine(self.expression).evaluate(data=scope)
        stack.pop()
        return result


class CircularReferenceException(Exception):
    pass
