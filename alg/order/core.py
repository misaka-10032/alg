# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Find kth smallest using random pivot.
"""

import random


def _bubble(ids, nums):
    _len = len(ids)
    for i in xrange(_len):
        for j in xrange(i-1, -1, -1):
            if nums[j] > nums[j+1]:
                ids[j], ids[j+1] = ids[j+1], ids[j]
                nums[j], nums[j+1] = nums[j+1], nums[j]
    return ids, nums


def _rough_median(ids, nums, step):
    _len = len(nums)
    if _len <= step:
        idx = _len // 2
        return ids[idx]
    mids, medians = [], []
    for i in xrange(0, _len, step):
        _step = step if i + step <= _len else (_len - i)
        ids[i:i+_step], nums[i:i+_step] = _bubble(ids[i:i+_step], nums[i:i+_step])
        idx = i + _step // 2
        _idx = idx if idx < _len else i
        mids.append(ids[_idx])
        medians.append(nums[_idx])
    return _rough_median(mids, medians, step)


def rough_median_pivot(a, p, q, step=5):
    return _rough_median(range(p, q), a[p:q], step)


def random_pivot(a, p, q):
    return random.randint(p, q-1)


def _find_kth(a, p, q, k, pivot_idx):
    """
    Find kth smallest in a within a[p:q]
    :param a:
    :param p:
    :param q:
    :param k:
    :param pivot_idx:
    :return:
    """
    """ Randomize to avoid worst case """
    x = pivot_idx(a, p, q)
    pivot = a[x]
    a[x] = a[p]
    a[p] = pivot
    """ r is current location of pivot """
    """ s is left idx """
    """ t is right idx """
    r, s, t = p, p, q-1
    while s < t:
        """ Backward first because it's ascending order.
        Consider: 20(p), 30, 1, 2, 3, 99, 100
        """
        while s < t and a[t] >= pivot:
            t -= 1
        a[r] = a[t]
        a[t] = pivot
        r = t
        """ Forward """
        while s < t and a[s] <= pivot:
            s += 1
        a[r] = a[s]
        a[s] = pivot
        r = s
    """ divide and conquer """
    if k < r:
        return _find_kth(a, p, r, k, pivot_idx)
    elif k > r:
        return _find_kth(a, r+1, q, k, pivot_idx)
    else:
        return pivot


def find_kth(a, k, pivot):
    """
    Find kth smalles in a
    :param a:
    :param k:
    :param pivot: either 'random' or 'median'
    :return:
    """
    if pivot == 'random':
        pivot_idx = random_pivot
    elif pivot == 'median':
        pivot_idx = rough_median_pivot
    else:
        raise NotImplementedError('Pivot type not supported!')
    return _find_kth(a, 0, len(a), k, pivot_idx)
