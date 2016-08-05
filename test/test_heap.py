# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Unit test for heaps.
"""

import numpy as np
from alg.heap import MinHeap, MaxHeap, MedHeap


def test_min_heap():
    a = np.random.choice(1000, 200, replace=False).tolist()
    b = sorted(a)
    """ test insert """
    heap = MinHeap()
    for x in a:
        heap.insert(x)
    c = []
    while heap:
        c.append(heap.pop().key)
    assert b == c
    """ test heapify """
    heap = MinHeap(a)
    c = []
    while heap:
        c.append(heap.pop().key)
    assert b == c


def test_max_heap():
    a = np.random.choice(1000, 200, replace=False).tolist()
    b = sorted(a, reverse=True)
    """ test insert """
    heap = MaxHeap()
    for x in a:
        heap.insert(x)
    c = []
    while heap:
        c.append(heap.pop().key)
    assert b == c
    """ test heapify """
    heap = MaxHeap(a)
    c = []
    while heap:
        c.append(heap.pop().key)
    assert b == c


def test_med_heap():
    a = np.random.choice(1000, 50, replace=False).tolist()
    """ test insert """
    heap = MedHeap()
    b = sorted(a)
    for x in a:
        heap.insert(x)
    while heap:
        x = heap.pop()
        m = len(b) / 2
        y = b.pop(m)
        assert x == y
    """ test heapify """
    heap = MedHeap(a)
    b = sorted(a)
    while heap:
        x = heap.pop()
        m = len(b) / 2
        y = b.pop(m)
        assert x == y
