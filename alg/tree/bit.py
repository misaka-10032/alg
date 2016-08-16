# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).

Binary Indexed Tree. Able to compute interval sums and update values.
Internal structure is [inclusive, exclusive).
API is [inclusive, inclusive]
"""


class BITree(object):
    def __init__(self, nums):
        self.nums = [0] * len(nums)
        self.sums = [0] * (len(nums) + 1)  # idx 0 is dummy
        for i in xrange(len(nums)):
            self[i] = nums[i]

    def __getitem__(self, i):
        return self.nums[i]

    def __setitem__(self, i, val):
        dv = val - self.nums[i]
        self.nums[i] = val
        k = i + 1
        while k < len(self.sums):
            self.sums[k] += dv
            k += k & -k

    def prefix_sum(self, i):
        k = i + 1
        s = 0
        while k > 0:
            s += self.sums[k]
            k -= k & -k
        return s

    def interval_sum(self, i, j):
        return self.prefix_sum(j) - self.prefix_sum(i-1)
