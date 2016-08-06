# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Base classes for heaps, aka priority queue.
Element is Node, whose key is taken as priority.
"""

from ..core import Node


class Heap(object):
    def __init__(self, list_=None, modifiable=False, debug=False):
        """
        :param list_: build a heap from list if passed in
        :param modifiable: support remove/update?
        :param debug: Print debug message
        """
        list_ = list_ or []
        self.L = map(lambda x: x if isinstance(x, Node) else Node(x), list_)
        self.modifiable = modifiable
        if modifiable:
            self.nid2idx = {id(node): idx for idx, node in enumerate(self.L)}
        self.debug = debug
        if len(self.L) > 0:
            self._build()

    def _best(self, *args):
        raise Exception("Not implemented")

    def _build(self):
        for i in xrange(len(self.L)/2, -1, -1):
            self._sift_down(i)

    def _left(self, idx):
        i = idx * 2 + 1
        return (i, self.L[i]) if i < len(self.L) else (None, None)

    def _right(self, idx):
        i = idx * 2 + 2
        return (i, self.L[i]) if i < len(self.L) else (None, None)

    def _parent(self, idx):
        i = (idx - 1) // 2
        return (i, self.L[i]) if i >= 0 else (None, None)

    def _sift_down(self, idx):
        old = self.L[idx]
        if self.debug:
            print 'Before sifting down', old
            print self

        tid, this = idx, self.L[idx]
        while True:
            lid, left = self._left(tid)
            rid, right = self._right(tid)
            best = self._best(this, left, right)
            if left and best is left:
                if self.modifiable:
                    self.nid2idx[id(left)] = tid
                    self.nid2idx[id(this)] = lid
                self.L[tid] = left
                self.L[lid] = this
                tid = lid
                continue
            elif right and best is right:
                if self.modifiable:
                    self.nid2idx[id(right)] = tid
                    self.nid2idx[id(this)] = rid
                self.L[tid] = right
                self.L[rid] = this
                tid = rid
                continue
            break

        if self.debug:
            print 'After sifting down', old
            print self

    def _bubble_up(self, idx):
        old = self.L[idx]
        if self.debug:
            print 'Before bubbling up', old
            print self

        tid, this = idx, self.L[idx]
        while True:
            pid, parent = self._parent(tid)
            best = self._best(this, parent)

            if parent and best is this:
                if self.modifiable:
                    self.nid2idx[id(parent)] = tid
                    self.nid2idx[id(this)] = pid
                self.L[tid] = parent
                self.L[pid] = this
                tid = pid
                continue
            break

        if self.debug:
            print 'After bubbling up', old
            print self

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
        if self.modifiable:
            self.nid2idx[id(this)] = tid
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
        popped = self.L.pop()
        if self.modifiable:
            self.nid2idx.pop(id(popped))
        if len(self.L) > 0:
            if self.modifiable:
                self.nid2idx[id(self.L[0])] = 0
            self._sift_down(0)

        if self.debug:
            print 'After popping:'
            print self

        return ret

    def peek(self):
        return self.L[0] if self else None

    def size(self):
        return len(self.L)

    def remove(self, node):
        if not self.modifiable:
            raise NotImplementedError(
                'The heap must be editable, see constructor.')
        idx = self.nid2idx[id(node)]
        self.nid2idx.pop(id(node))
        last = self.L.pop()

        if node is not last:
            self.L[idx] = last
            self.nid2idx[id(last)] = idx
            self._sift_down(idx)
            self._bubble_up(idx)

    def update(self, node, newkey):
        if not self.modifiable:
            raise NotImplementedError(
                'The heap must be editable, see constructor.')
        idx = self.nid2idx[id(node)]
        node.key = newkey
        self._sift_down(idx)
        self._bubble_up(idx)

    def __nonzero__(self):
        return len(self.L) > 0

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
