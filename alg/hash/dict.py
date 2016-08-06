# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Implements Dict. Support dynamic table with default threshold 2./3.
"""

from ..core import Node
from core import MulHash


class DictNode(Node):
    def __init__(self, key, value):
        super(DictNode, self).__init__(key, value)
        self.next = None


class Dict(object):
    def __init__(self, m=1024, alpha=2./3, Rhc=MulHash, debug=False):
        """
        :param m: initial # slots.
        :param alpha: load factor threshold.
        :param rhc: random hash class, must extend Hash.
        :return:
        """
        self.n = 0
        self.init_m = m
        self.m = m
        self.alpha = alpha
        self.Rhc = Rhc
        self.debug = debug
        self.rh = Rhc(m)
        self.H = [None] * m

    def hash(self, key):
        if isinstance(key, Node):
            key = key.key
        return self.rh.hash(key)

    def _lookup(self, key):
        idx = self.hash(key)
        prev = None
        curr = self.H[idx]
        while curr:
            if curr.key == key:
                break
            prev = curr
            curr = curr.next
        return idx, prev, curr

    def get(self, key):
        _, _, node = self._lookup(key)
        return node.value if node else None

    def __getitem__(self, item):
        return self.get(item)

    def _resize(self, size):
        _n, _m, _rh, _H = self.n, self.m, self.rh, self.H
        self.n = 0
        self.m = size
        self.rh = self.Rhc(size)
        self.H = [None] * size
        for node in _H:
            p = node
            while p:
                """ Tricky: p.next will be changed in _insert """
                q = p.next  # save it here
                idx = self.hash(p.key)
                self._insert(idx, p, extend=False)
                p = q

    def _insert(self, idx, node, extend=True):
        old = self.H[idx]
        self.H[idx] = node
        node.next = old
        """ Extend when necessary. """
        self.n += 1
        alpha = float(self.n) / self.m
        if extend and alpha > self.alpha:
            self._resize(self.m * 2)

    def put(self, key, value):
        idx, _, node = self._lookup(key)
        if node:
            node.value = value
        else:
            self._insert(idx, DictNode(key, value))

    def __setitem__(self, key, value):
        self.put(key, value)

    def pop(self, key):
        idx, prev, node = self._lookup(key)
        if not node:
            raise KeyError(key)
        if prev:
            prev.next = node.next
        else:
            self.H[idx] = node.next
        """ Shrink when necessary. """
        self.n -= 1
        alpha = float(self.n) / self.m
        if self.m >= self.init_m * 2 and alpha < self.alpha / 4:
            self._resize(self.m / 2)
        return node.value
