# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Red-black tree.
TODO: !!!!!!buggy!!!!!!!
"""
__author__ = 'misaka-10032'

from . import BsTree, BinNode


class RbNode(BinNode):
    RED = 'r'
    BLACK = 'b'

    def __init__(self, key=None, value=None, color=RED,
                 left=None, right=None, parent=None):
        super(RbNode, self).__init__(key, value, left, right, parent)
        self.color = color

    def _pretty_str(self):
        return '%s(%s)' % (self.key, self.color)

    def __repr__(self):
        return '%s\tcolor: %s\n' % \
               (super(RbNode, self).__repr__(), self.color)


class RbTree(BsTree):
    def _balance_insert(self, node):
        z = node
        RED = RbNode.RED
        BLACK = RbNode.BLACK

        while z and z.parent and z.parent.parent and z.parent.color == RED:
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.right
                if y and y.color == RED:        # case 1
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:                           # case 2
                    if z is z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color = BLACK      # case 3
                    z.parent.parent.color = RED
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y and y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._left_rotate(z.parent.parent)
        self.root.color = BLACK

    def insert(self, node, update=False):
        """
        Insert node into tree.
        :param node:
        :type node: RbNode
        :return:
        """
        if not isinstance(node, RbNode):
            node = RbNode(node)
        node = super(RbTree, self).insert(node, update)
        """ :type: RbNode """
        self._balance_insert(node)

        if self.debug:
            print 'After balancing:'
            print self
            print '*' * 20

        return node

    def __setitem__(self, key, value):
        self.insert(RbNode(key, value), update=True)

    @classmethod
    def _color(cls, node):
        return node.color if node else RbNode.BLACK

    def _balance_remove(self, node):
        x = node
        RED = RbNode.RED
        BLACK = RbNode.BLACK

        while x is not self.root and x.color == BLACK:
            if not x.parent:
                break
            if x is x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if self._color(w.left) == BLACK and \
                   self._color(w.right) == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if self._color(w.right) == BLACK:
                        if w.left:
                            w.left.color = BLACK
                        w.color = RED
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    if w.right:
                        w.right.color = BLACK
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if self._color(w.right) == BLACK and \
                   self._color(w.left) == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if self._color(w.left) == BLACK:
                        if w.right:
                            w.right.color = BLACK
                        w.color = RED
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    if w.left:
                        w.left.color = BLACK
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = BLACK

    def _remove(self, node, strategy):
        """
        Internal remove. Unbalance point is a bit different.
        :param node:
        :type node: BinNode
        :param strategy:
        :return ubp: the probable unbalanced point caused by deletion.
        """
        if not node:
            return
        if not node.left:
            self._transplant(node, node.right, True)
            return node
        if not node.right:
            self._transplant(node, node.left, True)
            return node

        if strategy == 'r':
            _min = self.min(node.right)
            _min = self._transplant(_min, _min.right, True)
            ubp = _min.parent if _min.parent is not node else _min
            self._transplant(node, _min, False)
            return ubp
        else:
            _max = self.max(node.left)
            _max = self._transplant(_max, _max.left, True)
            ubp = _max.parent if _max.parent is not node else _max
            self._transplant(node, _max, False)
            return ubp

    def remove(self, node, strategy='r'):
        if not isinstance(node, RbNode):
            node = self.search(node)

        if self.debug:
            print '*' * 20
            print 'delete node'
            print node
            print 'Before deletion:'
            print self

        old_color = node.color
        ubp = self._remove(node, strategy)
        """ :type: RbNode """
        if old_color == RbNode.BLACK:
            self._balance_remove(ubp)

        if self.debug:
            print 'Unbalanced point was:'
            print ubp
            print 'After balancing:'
            print self
            print '*' * 20

        return node
