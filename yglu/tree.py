''' Model for the internal document structure. '''

from collections import OrderedDict


class Document:
    def __init__(self):
        self.filepath = None
        self.root = None
        self.currentPath = []


class Node:
    def __init__(self, doc):
        self.visible = True
        self.memo = None
        self.doc = doc

    def content(self):
        if(self.memo is None):
            self.memo = self.create_content()
        return self.memo

    def create_content(self):
        return self


class MergeKey:
    def merge(self, parent, source):
        if isinstance(source, OrderedDict):
            parent.update(OrderedDict.items(source))
        elif isinstance(source, dict):
            parent.update(source)
        elif isinstance(source, list):
            parent.update(list.items(source))


class Scalar(Node):
    def __init__(self, value, doc=None):
        Node.__init__(self, doc)
        self.memo = value

    def content(self):
        return self.memo

    def __repr__(self):
        return str(self.memo)


class Mapping(OrderedDict, Node):
    def __init__(self):
        Node.__init__(self, None)

    def __init__(self, source=None, doc=None):
        Node.__init__(self, doc)
        self.special_entries = []
        if source:
            if isinstance(source, OrderedDict):
                source = OrderedDict.items(source)
            elif isinstance(source, dict):
                source = dict.items(source)
            OrderedDict.__init__(self, self.handle_keys(source))

    def __getitem__(self, key):
        if(self.__contains__(key)):
            return super().__getitem__(key).content()
        else:
            return self.resolve_special(key)

    def items(self):
        self.resolve_special()
        items = filter(lambda kv: kv[1].visible and kv[1].content() is not None,
                       super().items())
        return [(k, v.content()) for (k, v) in items]

    def __eq__(self, other):
        return dict(self.items()) == other

    def __repr__(self):
        return 'y'+dict(self.items()).__repr__()

    def handle_keys(self, items):
        for (k, v) in items:
            if isinstance(k, Scalar):
                yield (k.content(), v)
            else:
                self.special_entries.insert(0, (k, v))

    def resolve_special(self, key=None):
        while len(self.special_entries) > 0:
            (k, v) = self.special_entries.pop()
            if isinstance(k, MergeKey):
                k.merge(self, v)
            else:
                computed_key = k.content()
                if computed_key is not None:
                    self[computed_key] = v
                else:
                    raise Exception("mapping key is null")
        self.special_entries = []
        return self.get(key)


class Sequence(list, Node):
    def __init__(self, value=None, doc=None):
        Node.__init__(self, doc)
        if value:
            list.__init__(self, value)

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
