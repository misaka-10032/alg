# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Base classes for trees.
Many use `not node` rather than `node is not None` is because
we want to support `NilNode`, though not None, still False.
"""

from ..core import Node, print_node


class BinNode(Node):
    def __init__(self, key, val=None,
                 left=None, right=None, parent=None):
        super(BinNode, self).__init__(key, val)
        self.left = left
        self.right = right
        self.parent = parent


class BinTree(object):
    ORDER_PRE = 'pre'
    ORDER_IN = 'in'
    ORDER_POST = 'post'

    def __init__(self, node=None, debug=False):
        self.root = node
        self.debug = debug

    def traverse(self, order=ORDER_IN, node=None, func=print_node):
        start = node or self.root
        if order == self.ORDER_PRE:
            self._traverse_pre(start, func)
        elif order == self.ORDER_IN:
            self._traverse_in(start, func)
        elif order == self.ORDER_POST:
            self._traverse_post(start, func)
        else:
            raise Exception("""Order should be one of the following:
            %s.ORDER_PRE, %s.ORDER_IN, %s.ORDER_POST.
            """ % (self.__class__.__name__,
                   self.__class__.__name__,
                   self.__class__.__name__))

    def _traverse_pre(self, node, func):
        if not node:
            return
        if func:
            func(node)
        self._traverse_pre(node.left, func)
        self._traverse_pre(node.right, func)

    def _traverse_in(self, node, func):
        if not node:
            return
        self._traverse_in(node.left, func)
        if func:
            func(node)
        self._traverse_in(node.right, func)

    def _traverse_post(self, node, func):
        if not node:
            return
        self._traverse_post(node.left, func)
        self._traverse_post(node.right, func)
        if func:
            func(node)

    @classmethod
    def _pretty_str(cls, node):
        if not node:
            return [], 0, 0
        label = node._pretty_str()
        if not node.left:
            left_lines, left_pos, left_width = [], 0, 0
        else:
            left_lines, left_pos, left_width = cls._pretty_str(node.left)
        if not node.right:
            right_lines, right_pos, right_width = [], 0, 0
        else:
            right_lines, right_pos, right_width = cls._pretty_str(node.right)
        middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
        pos = left_pos + middle // 2
        width = left_pos + middle + right_width - right_pos
        while len(left_lines) < len(right_lines):
            left_lines.append(' ' * left_width)
        while len(right_lines) < len(left_lines):
            right_lines.append(' ' * right_width)
        if (middle - len(label)) % 2 == 1 and node.parent is not None and \
           node is node.parent.left and len(label) < middle:
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

    def pretty_str(self, node=None):
        node = node or self.root
        return '\n'.join(self._pretty_str(node)[0])

    def pretty_print(self, node=None):
        print self.pretty_str(node)

    def __repr__(self):
        return self.pretty_str()


class BsTree(BinTree):
    """
    Binary search tree. Duplicate key not supported.
    """
    @classmethod
    def min_at(cls, start):
        if not start:
            return None
        while start.left:
            start = start.left
        return start

    def min(self, start=None):
        start = start or self.root
        return self.min_at(start)

    @classmethod
    def max_at(cls, start):
        if not start:
            return
        while start.right:
            start = start.right
        return start

    def max(self, start=None):
        start = start or self.root
        return self.max_at(start)

    def _search(self, start, key):
        if not start:
            return None
        if key == start.key:
            return start
        if key < start.key:
            return self._search(start.left, key)
        else:
            return self._search(start.right, key)

    def search(self, key, start=None):
        start = start or self.root
        return self._search(start, key)

    def __getitem__(self, item):
        return self.search(item).val

    def __contains__(self, item):
        return bool(self.search(item))

    def next(self, node):
        if not isinstance(node, BinNode):
            node = self.search(node)
        if not node:
            return
        if node.right:
            return self.min(node.right)
        parent = node.parent
        while parent and node is parent.right:
            node = parent
            parent = parent.parent
        return parent

    def prev(self, node):
        if not isinstance(node, BinNode):
            node = self.search(node)
        if not node:
            return
        if node.left:
            return self.max(node.left)
        parent = node.parent
        while parent and node is parent.left:
            node = parent
            parent = parent.parent
        return parent

    def _left_rotate(self, node):
        """
        Rotate node from parent to left child.
        :param node:
        :return: node
        """
        if self.debug:
            print '*' * 20
            print 'left rotate node'
            print node
            print 'Before rotation:'
            print self

        """ For later ref.
        Ref by name, don't by field. """
        x = node
        z = x.parent
        y = x.right
        B = y.left
        """ Update edges """
        if z:
            if x is z.left:
                z.left = y
            else:
                z.right = y
        else:
            self.root = y
        y.parent = z
        y.left = x
        x.parent = y
        x.right = B
        if B is not None:
            B.parent = x

        if self.debug:
            print 'After rotation:'
            print self
            print '*' * 20

        return node

    def _right_rotate(self, node):
        """
        Rotate node from left child to parent.
        :param node:
        :return: node
        """
        if self.debug:
            print '*' * 20
            print 'right rotate node'
            print node
            print 'Before rotation:'
            print self

        """ For later ref.
        Ref by name, don't by field. """
        x = node.left
        y = node
        z = y.parent
        B = x.right
        assert x is y.left
        """ Update edges """
        if z:
            if y is z.left:
                z.left = x
            else:
                z.right = x
        else:
            self.root = x
        x.parent = z
        x.right = y
        y.parent = x
        y.left = B
        if B is not None:
            B.parent = y

        if self.debug:
            print 'After rotation:'
            print self
            print '*' * 20

        return node

    def insert(self, node, update=False):
        """
        Insert a new node into the tree. N.B. don't attempt to insert a subtree.
        :param node: the new node to be inserted.
        :type node: BinNode
        :param update: whether update the original val if key exists.
        :return: the inserted node.
        :rtype: BinNode
        """
        if not isinstance(node, BinNode):
            node = BinNode(node)

        if self.debug:
            print '*' * 20
            print 'Insert node'
            print '*' * 20
            print node
            print 'Before insertion:'
            print self

        """ Probe parent.
        Parent should be the next larger node than the inserted node.
        """
        parent = None
        probe = self.root
        while probe:
            parent = probe
            if node.key < probe.key:
                probe = probe.left
            else:
                probe = probe.right

        """ Insert node. """
        ret = node
        node.parent = parent
        if not parent:
            self.root = node
        elif node.key < parent.key:
            parent.left = node
        elif node.key > parent.key:
            parent.right = node
        else:
            if update:
                parent.val = node.val
                ret = None
            else:
                raise KeyError("Duplicate key: %s" % node.key)

        if self.debug:
            print 'After insertion:'
            print self
            print '*' * 20

        return ret

    def __setitem__(self, key, val):
        self.insert(BinNode(key, val), update=True)

    def _transplant(self, old, new, carry=True):
        """
        Transplant the old node with new node.
        :param old:
        :param new:
        :param carry: whether the new node should carry its descendants.
        :return: old
        """
        if self.debug:
            print '*' * 20
            print 'Transplant old'
            print old
            print 'with new'
            print new
            print 'Before transplanting:'
            print self

        if not old.parent:
            self.root = new
        elif old is old.parent.left:
            old.parent.left = new
        else:
            old.parent.right = new

        # tricky: can also set parent for NilNode
        if new is not None:
            new.parent = old.parent

        if new and not carry:
            if new is not old.left:
                new.left = old.left
                if old.left:
                    old.left.parent = new
            if new is not old.right:
                new.right = old.right
                if old.right:
                    old.right.parent = new

        if self.debug:
            print 'After transplanting:'
            print self
            print '*' * 20

        return old

    def _remove(self, node, strategy):
        """
        Internal remove
        :param node:
        :type node: BinNode
        :param strategy:
        :return ubp: the probable unbalanced point caused by deletion.
        """
        if not node:
            return
        if not node.left:
            self._transplant(node, node.right, True)
            return node.parent
        if not node.right:
            self._transplant(node, node.left, True)
            return node.parent

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
        """
        Delete a node from tree.
        :param node: the node to be deleted.
        :param strategy: either 'r' or 'l'; default as 'r'.
        :return: the deleted node, with parent, left and right preserved.
                 None if nonexistent.
        """
        if not isinstance(node, BinNode):
            node = self.search(node)

        if self.debug:
            print '*' * 20
            print 'Remove node'
            print node
            print 'Before removing:'
            print self

        self._remove(node, strategy)

        if self.debug:
            print 'After removing:'
            print self
            print '*' * 20

        return node

    def pop(self, key):
        node = self.remove(key)
        return node.val
