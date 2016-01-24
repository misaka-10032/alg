# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Median heap
http://stackoverflow.com/a/10657732/3663161
"""
__author__ = 'misaka-10032'

from base import Node
from min import MinHeap
from max import MaxHeap


class MedHeap(object):
    def __init__(self, _list=None):
        self.maxheap = MaxHeap()
        self.minheap = MinHeap()
        if _list:
            for x in _list:
                self.insert(x)

    def insert(self, node):
        """
        Insert node into heap.
        :param node:
        ":type node: Node.
        :return: the inserted node.
        """
        if not isinstance(node, Node):
            node = Node(node)

        if not self.maxheap:
            return self.maxheap.insert(node)
        if not self.minheap:
            return self.minheap.insert(node)

        left = self.maxheap.peek()
        if node < left:
            self.maxheap.insert(node)
            if self.maxheap.size() > self.minheap.size() + 1:
                x = self.maxheap.pop()
                self.minheap.insert(x)
        else:
            self.minheap.insert(node)
            if self.minheap.size() > self.maxheap.size() + 1:
                x = self.minheap.pop()
                self.maxheap.insert(x)
        return node

    def pop(self):
        """
        Pop ONE element from the heap.
        :return: If len is odd, return the median node.
                 If len is even, return mid-right first.
        """
        if self.maxheap.size() > self.minheap.size():
            return self.maxheap.pop()
        elif self.minheap.size() > self.maxheap.size():
            return self.minheap.pop()
        else:
            return self.minheap.pop()

    def peek(self):
        """
        Peak the median node.
        :return: If len is odd, return a single node.
                Otherwise return a tuple of two.
        """
        if not self.maxheap and not self.minheap:
            return None
        if self.maxheap.size() > self.minheap.size():
            return self.maxheap.peek()
        elif self.minheap.size() > self.maxheap.size():
            return self.minheap.peek()
        else:
            return self.maxheap.peek(), self.minheap.peek()

    def __nonzero__(self):
        return self.maxheap.size() > 0 or self.minheap.size() > 0

    def size(self):
        return self.maxheap.size() + self.minheap.size()
