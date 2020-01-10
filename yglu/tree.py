"""
Model for the internal document structure.
Collections accessors triggers the content creation of sub-nodes.
"""
from collections import OrderedDict

class Node:
    """ All elements of the tree are nodes"""
    visible = True 
    memo = None
    def content(self):
        if(memo is None)
            memo = self.create_content()
        return memo

class Scalar:
    def __init__(self, value):
        self.memo = value

class Mapping(Node, OrderedDict):
    def get_node(self, key):
        return OrderedDict.__getitem__(self, key)
    def __getitem__(self, key):
        return OrderedDict.__getitem__(self, key).content()
    def __setitem__(self, key, value):
        

class Sequence():
    pass
