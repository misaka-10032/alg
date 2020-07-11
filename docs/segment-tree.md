# Segment Tree

A segment tree is a data structure built on top of a fixed-length (n) array that is able to

* Answer min / max queries within a range in `O(log n)`.
* Update an element in `O(log n)`.
* Initialize in `O(n log n)`.

It has a variant to answer sum queries, but the binary indexed tree is more recommended for this case, because its initialization time is slightly faster (`O(n)`).
 
## Example

A node is represented as a range `[start, end)` in the array. It also holds the statistics (min / max) within the range.

```
           [0, 9)
       /            \
    [0, 4)          [4, 9)
    /    \          /    \
 [0, 2)  [2, 4)  [4, 6) [6, 9)
             ...
```
