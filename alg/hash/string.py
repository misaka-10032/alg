# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Hash related string matching.
"""

import random
from core import RollingHash
from primes import primes


def rabin_karp(sub, text, base=256, mod=None):
    """
    Find sub in text.
    :param sub:
    :param text:
    :param base: base used in hash func
    :param mod: magic number to be mod, should be prime.
    :return: list of matched positions
    """
    ret = []
    ls = len(sub)
    lt = len(text)
    if lt < ls:
        return ret
    mod = mod or primes[random.randint(10000, 100000)]
    rhs = RollingHash(sub, ls, base, mod)
    rht = RollingHash(text, ls, base, mod)
    i = 0
    while not rht.end():
        if rht.hash() == rhs.hash():
            if rht.window() == rhs.window():
                ret.append(i)
        i += 1
        rht.roll()
    return ret
