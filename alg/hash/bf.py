# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).

TODO: purpose
"""

import math
import random


class BloomFilter(object):
    def __init__(self, sz=10000, fp=.01, seed=10032):
        self.n_bits = int(2*sz*math.log(1./fp)+.5)
        self.n_hashes = int(1.5*math.log(1./fp)+.5)
        self.bits = 1 << self.n_bits
        rnd = random.Random()
        rnd.seed(seed)
        self.hash_masks = [0] * self.n_hashes
        for i in xrange(self.n_hashes):
            sign = random.choice([-1, 1])
            self.hash_masks[i] = sign * rnd.getrandbits(63)

    def hash_i(self, i, x):
        return (self.hash_masks[i] ^ hash(x)) % self.n_bits

    def add(self, x):
        # TODO: auto expand
        for i in xrange(self.n_hashes):
            self.bits |= 1 << self.hash_i(i, x)

    def __contains__(self, x):
        for i in xrange(self.n_hashes):
            if (self.bits >> self.hash_i(i, x)) % 2 == 0:
                return False
        return True

    def density(self):
        t = self.bits
        cnt = 0
        for _ in xrange(self.n_bits):
            if t % 2 == 1:
                cnt += 1
            t >>= 1
        return float(cnt) / self.n_bits
