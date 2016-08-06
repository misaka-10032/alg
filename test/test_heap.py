# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Unit test for heaps.
"""

import numpy as np
from alg.heap import MinHeap, MaxHeap, MedHeap


def test_min_heap():
    a = np.random.choice(1000, 200, replace=True).tolist()
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
    a = np.random.choice(1000, 200, replace=True).tolist()
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
    a = np.random.choice(1000, 50, replace=True).tolist()
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


def test_remove():
    n = 50
    a = np.random.choice(1000, n, replace=True).tolist()
    heap = MinHeap(a, modifiable=True)
    rm = np.random.choice(n, 10, replace=False).tolist()
    if n-1 not in rm:
        rm.append(n-1)
    nodes = [heap.L[i] for i in rm]
    for node in nodes:
        heap.remove(node)
    b = sorted(heap.L)
    c = []
    while heap:
        c.append(heap.pop())
    assert b == c


def test_update():
    n = 50
    a = np.random.choice(1000, n, replace=True).tolist()
    heap = MinHeap(a, modifiable=True)
    u_id = np.random.choice(n, 10, replace=False).tolist()
    u_val = np.random.choice(1000, 10, replace=True).tolist()
    if n-1 not in u_id:
        u_id.append(n-1)
        u_val.append(np.random.randint(1000))
    nodes = [heap.L[i] for i in u_id]
    for node, newkey in zip(nodes, u_val):
        heap.update(node, newkey)
    b = sorted(heap.L)
    c = []
    while heap:
        c.append(heap.pop())
    assert b == c
