# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Test cases for order statistics
"""
__author__ = 'misaka-10032'

import numpy as np
from pivot import find_kth, random_pivot, rough_median_pivot


def test_random_pivot():
    a = np.random.choice(1000, 600, replace=True).tolist()
    _a = sorted(a)
    k = np.random.randint(0, 100)
    kth = find_kth(a, k, pivot_idx=random_pivot)
    assert kth == _a[k]


def test_rough_median_pivot():
    a = np.random.choice(1000, 600, replace=True).tolist()
    _a = sorted(a)
    k = np.random.randint(0, 100)
    kth = find_kth(a, k, pivot_idx=rough_median_pivot)
    assert kth == _a[k]
