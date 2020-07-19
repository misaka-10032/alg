# Max Flow

### Concepts

* Capacity
* Flow
* Residual capacity
* Augmented path
* Relation between flow and residue: flow in one direction
  is residue on the other direction. Therefore, we may need
  to maintain the residues in both directions.

### Edmonds Karp

* Iteratively finding augmented path through bfs.
* Each time add the bottleneck residue to the total flow,
  and update the residues in the middle.

### BFS vs DFS

* DFS can be trapped into going through a bottleneck path
  once and once again.
* BFS won't have the problem, and guarantees the augmented
  path found in different iterations are non-increasing.

