# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

MaxHeap.
"""

from base import Heap


class MaxHeap(Heap):
    def _best(self, *args):
        return max(filter(lambda x: x, args))
