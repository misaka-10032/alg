# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Unit tests.
"""

from alg.hash import Dict
from alg.hash import rabin_karp
from alg.hash import BloomFilter


def test_dict():
    d = Dict(m=1)
    d['a'] = 1
    d['b'] = 2
    d['c'] = 3
    d['d'] = 4
    d[6.006] = 10032
    assert d['a'] == 1
    assert d['b'] == 2
    assert d['c'] == 3
    assert d['d'] == 4
    assert d[6.006] == 10032
    assert d.pop('a') == 1
    assert d.pop('b') == 2
    assert d.pop(6.006) == 10032
    assert d.pop('d') == 4
    assert d.pop('c') == 3


def test_rabin_karp():
    assert rabin_karp('aa', 'aaaa aabb abcc fdixsda') == [0, 1, 2, 5]
    assert rabin_karp('a', 'a') == [0]


def test_bf():
    bf = BloomFilter()
    bf.add('a')
    bf.add(1)
    bf.add(1234321)
    bf.add('xyz')
    # bf can give fp, so only check contains
    assert 'a' in bf
    assert 1 in bf
    assert 1234321 in bf
    assert 'xyz' in bf
