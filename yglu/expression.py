''' Node containing a YAQL expression to evaluate as content'''
import yaql
from .tree import Node

engine = yaql.factory.YaqlFactory().create(options={
    'yaql.convertInputData': False
})
scope = {}

def set_scope(new_scope):
    global scope
    scope = new_scope

class ExpressionNode(Node):    
    def __init__(self, expression):
        self.expression = expression

    def create_content(self):
        return engine(self.expression).evaluate(data=scope)
