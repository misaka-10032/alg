# Segment Tree

A segment tree is a data structure built on top of a fixed-length array `a[n]` that is able to

* Answer statistical queries (min, max, sum, etc.) within a range in `O(log n)`.
* Update an element in `O(log n)`.
* Initialize in `O(n log n)`.

The same functionality can be achieved by a binary indexed tree slightly more efficiently, but a segment tree is more readable.

## Example

A node is represented as a range `[start, end)` in the array. It also holds the statistics within the range.

```
           [0, 9)
       /            \
    [0, 4)          [4, 9)
    /    \          /    \
 [0, 2)  [2, 4)  [4, 6) [6, 9)
             ...
```
