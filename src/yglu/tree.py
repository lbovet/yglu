""" Model for the internal document structure. """

import os
from collections import OrderedDict


class Document:
    def __init__(self):
        self.filepath = None
        self.root = None
        self.errors = None


class Mark:
    def __init__(self, line, column):
        self.line = line
        self.column = column


class NodeException(Exception):
    def __init__(self, node, cause):
        self.node = node
        self.cause = cause

    def __str__(self):
        if self.node.doc.filepath is None:
            filepath = "<stdin>"
        else:
            filepath = os.path.relpath(self.node.doc.filepath, os.getcwd())

        start_mark = self.start_mark()

        if isinstance(self.cause, KeyError):
            message = "key not found: " + str(self.cause)
        else:
            message = str(self.cause)

        if not isinstance(self.cause, NodeException):
            if self.node.doc.filepath is None:
                message = (
                    message
                    + "\n in "
                    + filepath
                    + ", line "
                    + str(start_mark.line + 1)
                    + ", column "
                    + str(start_mark.column + 1)
                    + ":\n  "
                    + str(self.value())
                )
            else:
                message = (
                    filepath
                    + ":"
                    + str(start_mark.line + 1)
                    + ":"
                    + str(start_mark.column + 1)
                    + ":\n  "
                    + message
                    + ":\n   "
                    + str(self.value())
                )

        return message

    def value(self):
        if self.node.source is not None:
            return self.node.source.value

    def start_mark(self):
        if self.node.source is None:
            return Mark(0, 0)
        if self.node.source.start_mark.line == self.node.source.end_mark.line:
            column = self.node.source.end_mark.column - len(self.node.source.value)
            if hasattr(self.cause, "position") and self.cause.position:
                column += self.cause.position
                if self.node.source.value.startswith("."):
                    column -= 2
        else:
            column = self.node.source.start_mark.column
        return Mark(self.node.source.start_mark.line, column)

    def end_mark(self):
        if self.node.source is None:
            return Mark(0, 0)
        return self.node.source.end_mark


class Node:
    def __init__(self, doc, source=None):
        self.visible = True
        self.memo = None
        self.doc = doc
        self.source = source

    def content(self):
        if self.memo is None:
            self.memo = self.create_content()
        return self.memo

    def create_content(self):
        return self

    def receive(self, visitor):
        visitor(self.content())


class MergeKey:
    def __init__(self):
        self.visited = False

    def merge(self, parent, source):
        self.visited = True
        if isinstance(parent, Mapping):
            if isinstance(source, OrderedDict):
                parent.update(OrderedDict.items(source))
            elif isinstance(source, dict):
                parent.update(source)
            elif isinstance(source, Node):
                self.merge(parent, source.content())
            if isinstance(source, Mapping):
                parent.special_entries.extend(source.special_entries)
        else:
            if isinstance(source, OrderedDict):
                parent.append(OrderedDict.items(source))
            elif isinstance(source, dict):
                parent.append(source)
            elif isinstance(source, Node):
                self.merge(parent, source.content())
            else:
                parent.extend(source)


class Scalar(Node):
    def __init__(self, value, doc=None):
        Node.__init__(self, doc)
        self.memo = value

    def content(self):
        return self.memo

    def __repr__(self):
        return str(self.memo)


class Mapping(OrderedDict, Node):
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
        if self.__contains__(key):
            return super().__getitem__(key).content()
        else:
            return self.resolve_special(key)

    def items(self):
        self.resolve_special()
        for (k, v) in super().items():
            if isinstance(v, Node):
                result = (k, v.content())
                if v.visible:
                    yield result
            elif v is not None:
                yield (k, v)

    def __eq__(self, other):
        return dict(self.items()) == other

    def __repr__(self):
        return "<mapping>"

    def receive(self, visitor):
        for (k, v) in self.items():
            if isinstance(v, Node):
                v.receive(visitor)
            else:
                visitor(v)

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
                    raise NodeException(k, "mapping key is null")
        self.special_entries = []
        if key is not None:
            return super().__getitem__(key)


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
                node = iter.__next__()
                if (
                    isinstance(node, Mapping)
                    and len(node) == 0
                    and len(node.special_entries) == 1
                ):
                    (k, v) = node.special_entries[0]
                    if not k.visited:
                        k.merge(self, v)
                elif isinstance(node, Node):
                    if node.content() is not None and node.visible:
                        yield node.content()
                else:
                    yield node
        except StopIteration:
            return

    def __repr__(self):
        return "<sequence>"

    def receive(self, visitor):
        for v in self:
            if isinstance(v, Node):
                v.receive(visitor)
            else:
                visitor(v)
