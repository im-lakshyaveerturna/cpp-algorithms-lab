# B.Tech CSE — Design and Analysis of Algorithms Lab (C++17)

Seven standalone, commented C++ programs for the requested DAA practicals,
covering divide and conquer, graph traversal, greedy algorithms and dynamic
programming. The presentation follows a typical Indian B.Tech CSE lab format:
aim, algorithm, input/output and complexity. Individual universities may use
different experiment numbers or input conventions; the requested numbering
(1–6 and 13) is preserved here.

| Experiment | Program | Technique | Time complexity |
| --- | --- | --- | --- |
| 1 | [Strassen's multiplication](programs/01_strassen.cpp) | Divide and conquer | O(N^log₂7), about O(N^2.807) |
| 2 | [Breadth-first search](programs/02_bfs.cpp) | Queue-based adjacency-list traversal | O(V + E) |
| 3 | [Depth-first search](programs/03_dfs.cpp) | Recursive adjacency-list traversal | O(V + E) |
| 4 | [Prim's MST](programs/04_prim.cpp) | Greedy, min-heap | O(V + E log(E + 1)) |
| 5 | [Dijkstra's shortest paths](programs/05_dijkstra.cpp) | Greedy, min-heap | O(V + E log(E + 1)) |
| 6 | [Weighted interval scheduling](programs/06_weighted_interval_scheduling.cpp) | Dynamic programming + binary search | O(n log n) |
| 13 | [0/1 knapsack](programs/13_zero_one_knapsack.cpp) | Dynamic programming | O(n(W + 1)) |

Here `N` is the next power of two at least as large as the matrix order, `V` and
`E` are graph vertices and input edges, and `W` is knapsack capacity. Lazy heaps
can contain O(E) entries, so their bounds above also cover parallel edges.

## Compile and run

Use GCC, Clang, or another C++17 compiler. Each `.cpp` file has its own `main()`
and can be compiled independently; do not link all seven files into one program.
The code uses standard headers, with no external libraries or `bits/stdc++.h`.

```sh
mkdir -p build
c++ -std=c++17 -O2 -Wall -Wextra -Wpedantic programs/01_strassen.cpp -o build/01_strassen
./build/01_strassen < samples/01_strassen.in
```

Replace `01_strassen` with the corresponding filename stem for another program.
Strassen, Prim, Dijkstra, weighted interval scheduling and knapsack read
whitespace-separated input without interactive prompts. You can run those
executables without redirection and type their input. BFS and DFS instead use
the reference's built-in graphs and require no keyboard input; their `.in`
sample files are empty.

On Windows with MinGW, use `g++` in place of `c++`, choose an `.exe` output name,
and run it in Command Prompt with the same `< samples/...in` redirection.

## Common graph conventions

- Vertex IDs are **0-based**.
- BFS, DFS and Prim use undirected graphs. Dijkstra supports either direction mode.
- BFS and DFS use the reference's built-in numeric graphs, begin at vertex 0,
  preserve edge insertion order, print the adjacency list and visit only the
  starting vertex's connected component. Edit their `edges` initialisers to
  change the demonstrations. Vertex count is inferred from the largest edge ID.
- Prim and Dijkstra retain their input formats and bounds:
  `1 <= V <= 100000`, `0 <= E <= 200000`.
- Self-loops and parallel edges are supported. BFS/DFS print each reachable
  vertex once. Their output loops safely handle disconnected and empty demos.

## 1. Strassen's matrix multiplication

**Aim:** Multiply two square integer matrices using divide and conquer.

**Algorithm:** Pad both matrices with zeros to a power-of-two order; divide each
into four quadrants; compute seven recursive products; combine the quadrants
and print only the original `n × n` result.

For quadrants `A11` through `A22` and `B11` through `B22`:

```text
M1 = (A11 + A22)(B11 + B22)    M2 = (A21 + A22)B11
M3 = A11(B12 - B22)           M4 = A22(B21 - B11)
M5 = (A11 + A12)B22           M6 = (A21 - A11)(B11 + B12)
M7 = (A12 - A22)(B21 + B22)
C11 = M1 + M4 - M5 + M7       C12 = M3 + M5
C21 = M2 + M4                C22 = M1 - M2 + M3 + M6
```

**Input:** `n`, then `n²` entries of A in row order, then `n²` entries of B.
Orders from 1 to 128 are supported, including non-powers of two. Entries must be
in `[-10000, 10000]`. These bounds keep even intermediate arithmetic within
signed 64-bit integers. Rectangular matrices are outside this practical's scope.

**Sample:** [input](samples/01_strassen.in) · [output](samples/01_strassen.out).
Multiplying `[[1,2],[3,4]]` by `[[5,6],[7,8]]` produces `[[19,22],[43,50]]`.

**Complexity:** `T(N) = 7T(N/2) + O(N²)`, so time is O(N^log₂7), with O(N²)
auxiliary space in this sequential recursive implementation. This educational
version recurses to order 1; small matrices may run faster with ordinary multiplication.

## 2. Breadth-first search (BFS)

**Aim:** Display graph vertices in breadth-first order, matching the reference's
[`Graphs/BFSadjLst.cpp`](https://github.com/Aayush-data-eng/Design-And-Analysis-of-Algorithm/blob/fb018e38df9ed2223aa6991af28c2b7294e8912f/Graphs/BFSadjLst.cpp).

**Algorithm:** Construct the adjacency list from the built-in undirected edges.
Mark and enqueue vertex 0. Repeatedly dequeue a vertex, record it and enqueue
its unvisited neighbours. Mark when enqueuing to avoid duplicate visits.

**Input:** No keyboard input. The reference edges are
`{{0,1}, {0,2}, {1,2}, {1,3}, {2,3}}`.
Neighbour order follows insertion order; it is not sorted.

**Output:** The reference's adjacency-list display and numeric BFS traversal
`0 1 2 3`. [Exact sample output](samples/02_bfs.out).
Run `./build/02_bfs` after compiling `programs/02_bfs.cpp`.

**Complexity:** O(V + E) traversal time and O(V) auxiliary traversal space;
adjacency-list storage is O(V + E).

## 3. Depth-first search (DFS)

**Aim:** Display graph vertices in depth-first order, matching the reference's
[`Graphs/dfsAdjacencyList.cpp`](https://github.com/Aayush-data-eng/Design-And-Analysis-of-Algorithm/blob/fb018e38df9ed2223aa6991af28c2b7294e8912f/Graphs/dfsAdjacencyList.cpp).

**Algorithm:** Construct the adjacency list, visit vertex 0 and recursively
explore each unvisited neighbour in edge insertion order. The traversal uses
recursion, as in the reference.

**Input:** No keyboard input. The reference edges are
`{{0,2}, {0,3}, {0,1}, {2,4}}`.

**Output:** The reference's adjacency-list display and numeric DFS traversal
`0 2 4 3 1`. [Exact sample output](samples/03_dfs.out).
Run `./build/03_dfs` after compiling `programs/03_dfs.cpp`.

**Complexity:** O(V + E) traversal time and O(V) auxiliary space, including
visited flags and the recursive call stack. Adjacency-list storage is O(V + E).

The source, built-in graphs, helper functions and console output follow upstream
commit `fb018e38df9ed2223aa6991af28c2b7294e8912f`; credit belongs to its author.
Corrections are limited to safe traversal-output bounds, an empty-demo guard,
success exit status and explicit size casts for warning-free C++17 compilation.
See [BFS_DFS_ALIGNMENT.md](BFS_DFS_ALIGNMENT.md) for details.

## 4. Prim's minimum spanning tree

**Aim:** Find a minimum spanning tree of a weighted undirected graph.

**Algorithm:** Begin at vertex 0. Use a min-heap to repeatedly choose the
lightest edge connecting an included vertex to an unvisited vertex. Ignore
obsolete candidates. If vertices remain in other components, restart to
construct a minimum spanning forest.

**Input:** `V E`, then `E` lines of `u v weight`. Weights are integers in
`[-10^9, 10^9]`; negative and zero weights are valid.

**Output:** Selected edges, total weight and component count. A disconnected
graph explicitly reports that no spanning tree exists and prints its minimum
spanning forest instead. A single vertex has an empty MST of weight zero.

**Sample:** [input](samples/04_prim.in) · [output](samples/04_prim.out).
The sample MST has total weight **19**.

**Complexity:** O(V + E log(E + 1)) time and O(V + E) total space.

## 5. Dijkstra's shortest paths

**Aim:** Find shortest-path distances from one source to every vertex.

**Algorithm:** Set the source distance to zero and all others to infinity.
Repeatedly extract the smallest tentative distance from a min-heap and relax
its outgoing edges. Skip heap entries superseded by a shorter distance.

**Input:** `V E directed`, where `directed` is `0` for undirected and `1` for
directed; then `E` lines of `u v weight`; then the source vertex ID.
Weights must be integers in `[0, 10^9]`. Negative weights are rejected because
Dijkstra's greedy assumption does not hold for them.

**Output:** Each vertex's distance and predecessor (`Parent`). `INF` means
unreachable; `-` means no predecessor. To recover a route, follow parent IDs
back to the source and reverse that sequence. Full routes are not printed for
every vertex because that output can be quadratic in graph size.

**Sample:** [input](samples/05_dijkstra.in) · [output](samples/05_dijkstra.out).
Distances from vertex 0 are `0, 3, 1, 4, INF`.

**Complexity:** O(V + E log(E + 1)) time and O(V + E) total space.

## 6. Weighted interval scheduling

**Aim:** Select non-overlapping jobs with maximum total profit.

**Algorithm:** Sort jobs by finish time. For each job, use binary search to
find how many earlier jobs finish by its start time. If that count is `p`, use
`best[i+1] = max(best[i], profit[i] + best[p])`. Backtrack to recover chosen jobs.

**Input:** `n`, then `n` lines of `start finish profit`. Jobs receive **1-based**
IDs in their original input order. Require `0 <= n <= 100000`,
`0 <= start < finish <= 10^9`, and profit in `[-10^9, 10^9]`.

Intervals are half-open: a job ending at time `t` is compatible with one
starting at `t`. Zero-duration jobs are rejected. Selecting no jobs is allowed;
negative-profit jobs are therefore optional. On equal profit, skip the current
job. Output IDs appear in chronological order.

**Sample:** [input](samples/06_weighted_interval_scheduling.in) ·
[output](samples/06_weighted_interval_scheduling.out).
Jobs **2 and 5** yield maximum profit **17**.

**Complexity:** O(n log n) time and O(n) auxiliary space.

## 13. 0/1 knapsack

**Aim:** Maximise total item value without exceeding capacity, selecting each
item at most once.

**Algorithm:** Let `best[i][w]` be the best value using the first `i` items with
capacity `w`. Either skip item `i`, or take it once if it fits:
`best[i][w] = max(best[i-1][w], value[i] + best[i-1][w-weight[i]])`.
Read only the previous row, then backtrack through the table for selected IDs.

**Input:** `n capacity`, then `n` lines of `weight value`. Item IDs are
**1-based** input positions. Require `0 <= n <= 200`, `0 <= capacity <= 10000`,
integer weights in `[0, 10^9]`, and integer values in `[-10^9, 10^9]`.

Items heavier than capacity are skipped. Zero-weight items, zero capacity,
empty input sets and negative values are supported. Every item can be used
at most once, including zero-weight items. Selecting nothing is allowed.
Ties skip the current item. These table-size bounds keep memory suitable for a lab.

**Sample:** [input](samples/13_zero_one_knapsack.in) ·
[output](samples/13_zero_one_knapsack.out).
Items **2 and 3** have total weight **50** and maximum value **220**.

**Complexity:** O(n(W + 1)) time and O((n + 1)(W + 1)) space. This is
pseudo-polynomial because it depends on the numeric capacity.

## Verification

```sh
python3 tests/test_algorithms.py
# Optional compiler override:
CXX=clang++ python3 tests/test_algorithms.py
# Optional runtime checks, if your compiler supports sanitizers:
CXX=clang++ CXXFLAGS='-fsanitize=address,undefined -fno-omit-frame-pointer' python3 tests/test_algorithms.py
```

The test script compiles all programs with C++17 and warnings treated as errors.
It checks exact sample outputs, invalid input, fixed-seed randomized cases,
non-power-of-two matrices, maximum matrix order/entry values, disconnected
graphs, reference traversal order, parallel edges, zero weights and empty optimisation problems.
Independent oracles use ordinary matrix multiplication, queue/recursive
traversals, Kruskal's algorithm, Floyd–Warshall, and exhaustive subset searches.
Tests also check recovered edges, predecessors, schedules and knapsack items.
GitHub Actions runs the suite on pushes and pull requests.

The five input-driven programs report invalid required input on standard error
and exit with a nonzero status. Their numeric bounds keep arithmetic within
signed 64-bit range and limit allocations. Whitespace separates their input
fields; trailing extra input is ignored. BFS and DFS use built-in graphs and
ignore standard input. These are teaching programs, not interactive menu applications.
