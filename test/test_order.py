# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Test cases for order statistics
"""

import numpy as np
from alg.order import find_kth


def test_random_pivot():
    a = np.random.choice(1000, 600, replace=True).tolist()
    _a = sorted(a)
    k = np.random.randint(0, 100)
    kth = find_kth(a, k, pivot='random')
    assert kth == _a[k]


def test_rough_median_pivot():
    a = np.random.choice(1000, 600, replace=True).tolist()
    _a = sorted(a)
    k = np.random.randint(0, 100)
    kth = find_kth(a, k, pivot='median')
    assert kth == _a[k]
