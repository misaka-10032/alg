# Binary Indexed Tree

A binary indexed tree is a data structure built on top of a fixed-length array `a[n]` that is able to

* Answer statistical queries (sum, min, max, etc.) within a range in `O(log n)`.
* Update an element in `O(log n)`.
* Initialize in `O(n)`.

For simplicity, we only include the implementation for sum queries. The implementation for min / max queries is move involved, because it requires two binary indexed trees.

## Example

Underneath is an example. A node is represented by its index.

```
   _____ 0 _________________________
  /   |     |       \               \
 1    2     4        8         ____ 16 ____               (1 bit)
      |    / \     / | \      /   |     |   \
      3   5   6   9  10 12   17   18    20   24           (2 bits)
              |      |  | \       |     | \
              7     11  13 14     19    21 22             (3 bits)
                           |               |
                           15              23             (4 bits)
```

## Tree structure

* Each node is keyed by its index.
* The `i`th level contains the indices with `i` bits, e.g.
  * The first layer has `1(1)`, `2(10)`, `4(100)`, `8(1000)`.
  * The second layer has `3(11)`, `5(101)`, `6(110)`, `9(1001)`, `10(1010)`.
  * The third layer has `7(111)`, `11(1011)`.
* Each node also stores the sum ranged from its parent index (inclusive) to itself (exclusive).
  * For example, `6` has parent `4`, so the node `6` stores `sum(a[4:6])`.

## Compute the prefix sum

* We start with the leaf node and sum up until the root node, e.g.

```
sum(a[4:7]) = sum(a[6:7]) + sum(a[4:6]) + sum(a[0:4])
```

## Compute the range sum

A range sum can be computed by two prefix sums.

```
sum(a[start:end]) = sum(a[:end]) - (sum(a[:start-1]) if start > 0 else 0)
```

## Find the parent

An easy way to tell the parent is to flip the rightmost 1, e.g.

* `11 = (1011)_2  -->  (1010)_2 = 10`
* `10 = (1010)_2  -->  (1000)_2 = 8`

Here's a trick to flip the rightmost 1.

* `x - (x & -x)`
* As we know `-x` is `~x+1`
* `&`ing that with original will only remain the rightmost `1`.

## Update a value

When the value of some index is updated, two types of nodes are affected:

* Its child nodes.
* The elder siblings of its non-root ancester.

For example, when `12(1100)` is updated, its child nodes include

* `13(1101)`, which contains `sum(a[12:13])`.
* `14(1110)`, which contains `sum(a[12:14])`.

Its non-root ancester `8(1000)` has the following elder siblings

* `16(10000)`, which contains `sum(a[:16])`.
* `32(100000)`, which contains `sum(a[:32])`.

These two types of nodes can be iterated with a bit operation:

* Add the rightmost 1 to the current index.

For example, we start with the first child `13(1101)` of `12(1100)`. We will iterate the following:

* `13(1101) + 1(0001) = 14(1110)`  (next sibling)
* `14(1110) + 2(0010) = 16(10000)` (next ancestor)
* `16(10000) + 16(10000) = 32(100000)` (next ancestor)

## Initialization

The prefix sum can be computed in `O(n)`. The sum on each node can be computed with the prefix sum in `O(1)`.
