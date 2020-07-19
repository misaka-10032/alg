# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

AvlTree.
"""

from core import (BsTree, BinNode)


class AvlNode(BinNode):
    def __init__(self, key=None, val=None,
                 left=None, right=None, parent=None):
        super(AvlNode, self).__init__(key, val, left, right, parent)
        self.height = None

    def _pretty_str(self):
        return '%s(%s)' % (self.key, self.height)

    def __repr__(self):
        return '%s\theight: %s\n' % \
               (super(AvlNode, self).__repr__(), self.height)


class AvlTree(BsTree):
    @classmethod
    def height(cls, node):
        if node:
            return node.height
        else:
            return -1

    @classmethod
    def _update_height(cls, node):
        node.height = 1 + max(cls.height(node.left), cls.height(node.right))
        return node

    def _left_rotate(self, node):
        super(AvlTree, self)._left_rotate(node)
        self._update_height(node)

        if self.debug:
            print 'After updating height:'
            print self
            print '*' * 20

        return node

    def _right_rotate(self, node):
        super(AvlTree, self)._right_rotate(node)
        self._update_height(node)

        if self.debug:
            print 'After updating height:'
            print self
            print '*' * 20

        return node

    def _balance(self, node):
        """
        Balance bottom up from node.
        :param node:
        :type node: AvlNode
        :return:
        """
        if self.debug:
            print '*' * 20
            print 'Balance node'
            print node
            print 'Before balancing:'
            print self

        while node:
            self._update_height(node)
            assert abs(self.height(node.right) - self.height(node.left)) <= 2
            if self.height(node.right) == self.height(node.left) + 2:
                if self.height(node.right.right) < self.height(node.right.left):
                    # case RL, reduce to case RR.
                    self._right_rotate(node.right)
                # case RR
                self._left_rotate(node)
            elif self.height(node.left) == self.height(node.right) + 2:
                if self.height(node.left.left) < self.height(node.left.right):
                    # case LR, reduce to case LL.
                    self._left_rotate(node.left)
                # case LL
                self._right_rotate(node)
            node = node.parent

        if self.debug:
            print 'After balancing:'
            print self
            print '*' * 20

    def insert(self, node, update=False):
        """
        Insert node into tree.
        :param node:
        :type node: AvlNode
        :return:
        """
        if not isinstance(node, AvlNode):
            node = AvlNode(node)

        node = super(AvlTree, self).insert(node, update)
        """ :type: AvlNode """
        self._balance(node)

        return node

    def __setitem__(self, key, val):
        self.insert(AvlNode(key, val), update=True)

    def remove(self, node, strategy='r'):
        """
        Delete a node from tree.
        :param node: the node to be deleted.
        :param strategy: either 'r' or 'l'; default as 'r'.
        :return: the deleted node, with parent, left and right preserved.
                 None if nonexistent.
        """
        if not isinstance(node, AvlNode):
            node = self.search(node)

        if self.debug:
            print '*' * 20
            print 'Remove node'
            print node
            print 'Before removing:'
            print self

        ubp = self._remove(node, strategy)
        """ :type: AvlNode """
        self._balance(ubp)

        if self.debug:
            print 'Unbalanced point was:'
            print ubp
            print 'After removing:'
            print self
            print '*' * 20

        return node
