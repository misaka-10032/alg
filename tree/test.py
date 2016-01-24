# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Test cases for tree package. Uses nose2.
"""
__author__ = 'misaka-10032'

import numpy as np
from . import BsTree
from . import AvlTree
from . import RbTree, RbNode


def _test_bst_node(node):
    left = node.left
    right = node.right
    if not left or not right:
        return
    assert BsTree.max_at(left) <= node <= BsTree.min_at(right)


def _test_bst(tree):
    """
    :type tree: BsTree
    """
    a = np.random.choice(1000, 20, replace=False).tolist()
    b = sorted(a)
    """ test insert """
    for x in a:
        tree.insert(x)
    tree.traverse(order=tree.ORDER_IN, func=_test_bst_node)
    c = []
    t2l = lambda node: c.append(node.key)
    tree.traverse(order=tree.ORDER_IN, func=t2l)
    assert b == c
    """ test delete """
    d = np.random.choice(b, 10, replace=False).tolist()
    for x in d:
        b.remove(x)
        tree.remove(x)
    c = []
    t2l = lambda node: c.append(node.key)
    tree.traverse(order=tree.ORDER_IN, func=t2l)
    assert b == c
    return tree


def test_bst():
    _test_bst(BsTree())


def _test_avl_node(node):
    assert abs(AvlTree.height(node.left) - AvlTree.height(node.right)) <= 1, \
        'node\n%s\nviolates avl property.' % node


def test_avl():
    tree = _test_bst(AvlTree())
    """ test avl property """
    tree.traverse(order=tree.ORDER_IN, func=_test_avl_node)


def _test_rb_node(node):
    if node.color == RbNode.RED and node.parent:
        assert node.parent.color == RbNode.BLACK, \
        'node\n%s\nshould have a black parent' % node
    # TODO: check same # of black's in the path down.


# TODO
# def test_rb():
#     tree = _test_bst(RbTree(debug=True))
#     """ test rb property """
#     tree.traverse(order=tree.ORDER_IN, func=_test_rb_node)
