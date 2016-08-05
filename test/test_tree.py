# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Test cases for tree package. Uses nose2.
"""

import numpy as np
from alg.tree import rb
from alg.tree import BsTree, AvlTree, RbTree


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
    # check red has black parent
    if node.color == 'r' and node.parent:
        assert node.parent.color == 'b', \
        'node\n%s\nshould have a black parent' % node

    # check same # of black's in the path down.
    # left height
    if not node.left:
        h_left = 1
    else:
        if node.left.color == rb.BLACK:
            h_left = 1 + node.left.val
        else:
            h_left = node.left.val
    # right height
    if not node.right:
        h_right = 1
    else:
        if node.right.color == rb.BLACK:
            h_right = 1 + node.right.val
        else:
            h_right = node.right.val
    # assert left height == right height
    assert h_left == h_right, \
        'h_left({}) != h_right({}) for node\n{}'.format(
            h_left, h_right, node)
    node.val = h_left


def test_rb():
    tree = _test_bst(RbTree())
    """ test rb property """
    assert tree.root.color == rb.BLACK
    tree.traverse(order=tree.ORDER_POST, func=_test_rb_node)
