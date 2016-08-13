# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Hash functions
"""

import random
import math
from sys import maxint


class MulHash(object):
    """
    Random func based on mul. Hopefully universal, maybe not.
    """
    def __init__(self, m):
        self.a = random.randint(1, maxint)
        self.w = int(math.log(maxint))
        self.r = int(math.log(m, 2))

    def hash(self, key):
        k = hash(key)
        return int(((self.a * k) % (1 << self.w)) >> (self.w - self.r))


class RollingHash(object):
    def __init__(self, text, winsz, base, mod):
        self.text = text
        self.winsz = winsz
        self.base = base
        self.mbase = base ** (winsz - 1)
        self.mod = mod
        self.rh = 0
        for i in xrange(0, winsz):
            self.rh *= base
            self.rh += ord(text[i])
            self.rh %= mod
        self.pos = winsz

    def roll(self):
        if self.pos == len(self.text):
            self.pos += 1
            return
        self.rh -= ord(self.text[self.pos - self.winsz]) * self.mbase
        self.rh *= self.base
        self.rh += ord(self.text[self.pos])
        self.rh %= self.mod
        self.pos += 1

    def end(self):
        return self.pos > len(self.text)

    def hash(self):
        return self.rh

    def window(self):
        return self.text[self.pos-self.winsz:self.pos]
