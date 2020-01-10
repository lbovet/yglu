'''
Model for the internal document structure.
Node content can be the result of a computation.
'''
from collections import OrderedDict


class Node:
    visible = True
    memo = None

    def content(self):
        if(self.memo is None):
            self.memo = self.create_content()
        return self.memo

    def create_content(self):
        return self


class Scalar(Node):
    def __init__(self, value):
        self.memo = value


class Mapping(Node, OrderedDict):
    def get_node(self, key):
        return super().__getitem__(key)

    def __getitem__(self, key):
        return super().__getitem__(key).content()

    def __items__(self):
        return self.content().__items__()

    def create_content(self):
        return {k: self[k] for k in self.keys()}


class Sequence(list, Node):
    def get_node(self, index):
        return super().__getitem__(self, index)

    def __getitem__(self, index):
        return super().__getitem__(index).content()

    def __iter__(self):
        return self.content().__iter__()

    def __eq__(self, value):
        return self.content.__eq__(value)

    def create_content(self):
        return [self[i] for i in range(len(self))]
