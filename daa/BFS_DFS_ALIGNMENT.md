# BFS and DFS reference alignment

Source: [Aayush-data-eng/Design-And-Analysis-of-Algorithm](https://github.com/Aayush-data-eng/Design-And-Analysis-of-Algorithm/tree/fb018e38df9ed2223aa6991af28c2b7294e8912f),
commit `fb018e38df9ed2223aa6991af28c2b7294e8912f`.

| Local program | Reference program |
|---|---|
| `programs/02_bfs.cpp` | `Graphs/BFSadjLst.cpp` |
| `programs/03_dfs.cpp` | `Graphs/dfsAdjacencyList.cpp` |

Credit for the reference code belongs to its author. Both programs retain the
reference's helpers, built-in edge lists, vertex-0 start and adjacency-list
display. BFS uses a queue; DFS uses recursion. Numeric vertex IDs replace the
previous user-supplied labels. Neighbours retain edge insertion order, and only
the starting component is traversed. Neither demonstration reads keyboard input.

The original main-program output is retained exactly for the supplied graphs,
including its labels, spaces and lack of a final newline. The sample `.in`
files are therefore empty. The sample `.out` files were captured from the
unmodified upstream demonstrations.

## Corrections

- Print `result.size()` or `resultant.size()` vertices instead of the inferred
  total graph size. A disconnected graph may have fewer reachable vertices;
  the original loops could read beyond the traversal vector.
- Skip the initial traversal when the built-in edge list describes no vertices.
  The original demonstrations attempted to access absent vertex 0.
- Return zero after successful execution instead of the reference's status 100.
- Cast vector sizes explicitly for warning-free signed loop comparisons.

Graph helpers retain the reference's preconditions: valid, nonnegative edge
endpoints within the constructed adjacency list, and a valid starting vertex
when calling traversal helpers directly. The demonstrations infer vertex count
from the maximum edge ID; isolated vertices beyond that ID are not encoded by
the edge-list initialiser. Recursive DFS uses O(V) call-stack space.

## Verification and scope

Tests check the exact reference demo output, insertion-order traversal against
independent Python queue/recursive traversals, cycles, parallel edges, self-loops,
isolated vertices, disconnected graphs and empty demonstrations. Alternate demo
edge lists are compiled to exercise the corrected main-program output bounds.
The same tests support AddressSanitizer and UndefinedBehaviorSanitizer through
the existing `CXXFLAGS` option.

Strassen, Prim, Dijkstra, weighted interval scheduling and 0/1 knapsack source
files and their samples remain unchanged from commit
`6043aff7a10db873dd2393eaff24d5a32d4d2789`.
