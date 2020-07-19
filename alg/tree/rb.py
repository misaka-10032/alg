# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Red-black tree.
"""

from . import BsTree, BinNode

RED = 'r'
BLACK = 'b'


class NilNode(BinNode):
    def __init__(self, parent):
        super(NilNode, self).__init__(None, None, None, None, parent)
        self.color = BLACK

    def __nonzero__(self):
        return False


class RbNode(BinNode):
    def __init__(self, key=None, val=None, color=RED,
                 left=None, right=None, parent=None):
        super(RbNode, self).__init__(key, val, left, right, parent)
        self.color = color
        if left is None:
            self.left = NilNode(self)
        if right is None:
            self.right = NilNode(self)

    def _pretty_str(self):
        return '%s(%s)' % (self.key, self.color)

    def __repr__(self):
        return '%s\tcolor: %s\n' % \
               (super(RbNode, self).__repr__(), self.color)


class RbTree(BsTree):
    def _balance_insert(self, node):
        z = node
        while z and z.parent and z.parent.parent and z.parent.color == RED:
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == RED:        # case 1
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
                if y.color == RED:
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
        :param update: if key is found, do we update its val?
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

    def __setitem__(self, key, val):
        self.insert(RbNode(key, val), update=True)

    def _balance_remove(self, node):
        x = node
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
                if w.left.color == BLACK and \
                   w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
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
                if w.right.color == BLACK and \
                   w.left.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
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
        y = z = node
        if not z.left:
            x = z.right
            self._transplant(z, z.right)
        elif not z.right:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self.min(z.right)
            old_color = y.color
            x = y.right
            if y.parent is z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if old_color == BLACK:
            self._balance_remove(x)

        if self.debug:
            print 'Unbalanced point was:'
            print x
            print 'After balancing:'
            print self
            print '*' * 20

        return node
