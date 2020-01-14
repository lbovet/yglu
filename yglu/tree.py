''' Model for the internal document structure. '''

from collections import OrderedDict


class Document:
    filepath = None
    root = None
    currentPath = []


class Node:
    visible = True
    memo = None
    doc = None

    def content(self):
        if(self.memo is None):
            self.memo = self.create_content()
        return self.memo

    def create_content(self):
        return self


class Scalar(Node):
    def __init__(self, value, doc=None):
        self.memo = value
        self.doc = doc


class Mapping(OrderedDict, Node):
    def __init__(self, value=None, doc=None):
        if value:
            super().__init__(value)
        self.doc = doc

    def get_node(self, key):
        return super().__getitem__(key)

    def __getitem__(self, key):
        return super().__getitem__(key).content()

    def items(self):
        items = filter(lambda kv: kv[1].visible, super().items())
        return [(k, v.content()) for (k, v) in items]

    def __eq__(self, other):
        return dict(self.items()) == other

    def __repr__(self):
        return 'y'+dict(self.items()).__repr__()


class Sequence(list, Node):
    def __init__(self, value=None, doc=None):
        if value:
            super().__init__(value)
        self.doc = doc

    def get_node(self, index):
        return super().__getitem__(self, index)

    def __getitem__(self, index):
        return super().__getitem__(index).content()

    def __eq__(self, other):
        return list(self) == other

    def __iter__(self):
        iter = super().__iter__()
        try:
            while True:
                next = iter.__next__()
                if next.visible:
                    yield next.content()
        except StopIteration:
            return

    def __repr__(self):
        return 'y'+list(self).__repr__()
