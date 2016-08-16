# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).

Segmentation tree, answering range query of min/max.
Internal representation is [inclusive, exclusive).
External API is [inclusive, inclusive].
"""


class SegNode(object):
    def __init__(self, lower, upper, val=0):
        """ [lower, upper) """
        self.lower = lower
        self.upper = upper
        self.val = val
        self.left = self.right = None


class SegTree(object):
    def __init__(self, nums, op='min'):
        """
        :param nums:
        :param op: either 'min' or 'max'
        """
        if op == 'min':
            self.op = min
        elif op == 'max':
            self.op = max
        else:
            raise NotImplementedError('Unsupported op!')
        assert nums
        self.root = self._build(0, len(nums)+1)
        for i, v in enumerate(nums):
            self[i] = v

    def _build(self, lower, upper):
        """ [lower, upper) """
        assert lower < upper
        if lower == upper-1:
            return SegNode(lower, upper)
        mid = (lower + upper) // 2
        node = SegNode(lower, upper)
        node.left = self._build(lower, mid)
        node.right = self._build(mid, upper)
        return node

    def _update(self, node, i, v):
        if node.lower == node.upper-1:
            node.val = v
            return v
        mid = (node.lower + node.upper) // 2
        if i < mid:
            new = self._update(node.left, i, v)
            node.val = self.op(new, node.right.val)
        else:
            new = self._update(node.right, i, v)
            node.val = self.op(new, node.left.val)
        return node.val

    def __setitem__(self, i, v):
        self._update(self.root, i, v)

    def _query(self, node, i, j):
        """ [i, j) inclusive, exclusive """
        if node.lower == node.upper-1:
            return node.val
        if i == node.lower and j == node.upper:
            return node.val
        mid = (node.lower + node.upper) // 2
        if j <= mid:
            return self._query(node.left, i, j)
        if i >= mid:
            return self._query(node.right, i, j)
        return self.op(self._query(node.left, i, mid),
                       self._query(node.right, mid, j))

    def range_query(self, i, j):
        """ [i, j] inclusive """
        return self._query(self.root, i, j+1)

    def __getitem__(self, i):
        return self._query(self.root, i, i+1)
