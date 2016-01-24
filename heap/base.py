# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Base classes for heaps
"""
__author__ = 'misaka-10032'

from ..common import Node


class Heap(object):
    def __init__(self, _list=None, debug=False):
        _list = _list or []
        self.L = map(lambda x: x if isinstance(x, Node) else Node(x), _list)
        self.debug = debug
        if len(self.L) > 0:
            self._build()

    def _best(self, *args):
        raise Exception("Not implemented")

    def _build(self):
        for i in xrange(len(self.L)/2, -1, -1):
            self._heapify(i)

    def _left(self, idx):
        i = idx * 2 + 1
        return (i, self.L[i]) if i < len(self.L) else (None, None)

    def _right(self, idx):
        i = idx * 2 + 2
        return (i, self.L[i]) if i < len(self.L) else (None, None)

    def _parent(self, idx):
        i = (idx - 1) // 2
        return (i, self.L[i]) if i >= 0 else (None, None)

    def _heapify(self, idx):
        tid, this = idx, self.L[idx]
        while True:
            lid, left = self._left(tid)
            rid, right = self._right(tid)
            best = self._best(this, left, right)
            if left and best is left:
                self.L[tid] = left
                self.L[lid] = this
                tid = lid
                continue
            elif right and best is right:
                self.L[tid] = right
                self.L[rid] = this
                tid = rid
                continue
            break

    def insert(self, node):
        if not isinstance(node, Node):
            node = Node(node)

        if self.debug:
            print '*' * 20
            print 'Insert node'
            print '*' * 20
            print node
            print 'Before inserting:'
            print self

        tid, this = len(self.L), node
        self.L.append(node)
        pid, parent = self._parent(tid)
        while parent:
            best = self._best(parent, this)
            if best is parent:
                break
            self.L[pid] = this
            self.L[tid] = parent
            tid = pid
            pid, parent = self._parent(tid)

        if self.debug:
            print 'After inserting:'
            print self
            print '*' * 20

        return node

    def pop(self):
        if self.debug:
            print '*' * 20
            print 'Pop node'
            print '*' * 20
            print self.L[0]
            print 'Before popping:'
            print self

        ret = self.L[0]
        self.L[0] = self.L[-1]
        self.L.pop()
        if len(self.L) > 0:
            self._heapify(0)

        if self.debug:
            print 'After popping:'
            print self

        return ret

    def peek(self):
        return self.L[0] if self else None

    def __nonzero__(self):
        return len(self.L) > 0

    def size(self):
        return len(self.L)

    def _pretty_str(self, idx):
        if idx < 0 or not self:
            return [], 0, 0
        tid, this = idx, self.L[idx]
        label = str(this._pretty_str())

        lid, left = self._left(idx)
        if left is None:
            left_lines, left_pos, left_width = [], 0, 0
        else:
            left_lines, left_pos, left_width = self._pretty_str(lid)

        rid, right = self._right(idx)
        if right is None:
            right_lines, right_pos, right_width = [], 0, 0
        else:
            right_lines, right_pos, right_width = self._pretty_str(rid)

        middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
        pos = left_pos + middle // 2
        width = left_pos + middle + right_width - right_pos
        while len(left_lines) < len(right_lines):
            left_lines.append(' ' * left_width)
        while len(right_lines) < len(left_lines):
            right_lines.append(' ' * right_width)

        pid, parent = self._parent(idx)
        if (middle - len(label)) % 2 == 1 and parent is not None and \
           this is self._left(pid)[1] and len(label) < middle:
            label += '.'
        label = label.center(middle, '.')
        if label[0] == '.':
            label = ' ' + label[1:]
        if label[-1] == '.':
            label = label[:-1] + ' '

        lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                 ' ' * left_pos + '/' + ' ' * (middle-2) +
                 '\\' + ' ' * (right_width - right_pos)] + \
                [left_line + ' ' * (width - left_width - right_width) + right_line
                    for left_line, right_line in zip(left_lines, right_lines)]
        return lines, pos, width

    def pretty_str(self, idx=0):
        return '\n'.join(self._pretty_str(idx)[0])

    def pretty_print(self, idx=0):
        print self.pretty_str(idx)

    def __repr__(self):
        return self.pretty_str()
