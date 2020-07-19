# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Base classes.
"""


class Node(object):
    def __init__(self, key, val=None):
        self.key = key
        self.val = val

    def _pretty_str(self):
        return self.key

    def __repr__(self):
        return '%s\n\tkey: %s\n\tvalue: %s\n' % \
               (super(Node, self).__repr__(), self.key, self.val)

    def __cmp__(self, other):
        if isinstance(other, Node):
            return cmp(self.key, other.key)
        else:
            return cmp(self.key, other)

    def __hash__(self):
        return hash(self.key)


def print_node(node):
    print node
