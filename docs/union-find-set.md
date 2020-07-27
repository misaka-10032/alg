# Union-Find Set

A [union-find set](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) is a set-like data structure that allows
efficient connectivity queries. It supports the following operations:

* `add(key)`: Add a key to the set.
* `find(key)`: Find the representative of the component that the key belongs to.
* `union(key1, key2)`: Joins the two components that `key1` and `key2` belong to respectively. A new representative will
  be elected if `key1` and `key2` belongs to two different components.

The data structure consists of two maps.

* `parents`: Maps a key to its parent key. Following the map we can find the representative of the component.
* `ranks`: Tracks the ranks of the **root** keys. It is a proxy of the depth of the tree (it can change later during
  `find()` queries). This `rank` provides guidance in how to elect a new representative during `union()`: putting the
  low-rank tree under a high-rank tree produces a shorter tree, and therefore is more friendly for `find()` queries.

It is efficient for **sparse** `find()` queries. If the query is dense enough, e.g. for all the nodes, then DFS or BFS is preferred.

## Example Problems

https://leetcode.com/problems/accounts-merge/
