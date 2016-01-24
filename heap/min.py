# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

MinHeap.
"""
__author__ = 'misaka-10032'

from base import Heap


class MinHeap(Heap):
    def _best(self, *args):
        return min(filter(lambda x: x, args))
