// Experiment 5: Dijkstra's single-source shortest-path algorithm.
#include <functional>
#include <iostream>
#include <limits>
#include <queue>
#include <utility>
#include <vector>

int main() {
    int n, m, directed;
    if (!(std::cin >> n >> m >> directed) || n < 1 || n > 100000 ||
        m < 0 || m > 200000 || (directed != 0 && directed != 1)) {
        std::cerr << "Error: require 1..100000 vertices, 0..200000 edges, directed flag 0 or 1.\n";
        return 1;
    }
    std::vector<std::vector<std::pair<int, long long>>> graph(n);
    for (int i = 0; i < m; ++i) {
        int u, v;
        long long w;
        if (!(std::cin >> u >> v >> w) || u < 0 || u >= n || v < 0 || v >= n ||
            w < 0 || w > 1000000000LL) {
            std::cerr << "Error: invalid vertex or weight; Dijkstra requires weights in [0, 10^9].\n";
            return 1;
        }
        graph[u].emplace_back(v, w);
        if (!directed) graph[v].emplace_back(u, w);
    }
    int source;
    if (!(std::cin >> source) || source < 0 || source >= n) {
        std::cerr << "Error: invalid source vertex.\n";
        return 1;
    }
    const long long infinity = std::numeric_limits<long long>::max() / 4;
    std::vector<long long> distance(n, infinity);
    std::vector<int> parent(n, -1);
    using Entry = std::pair<long long, int>;
    std::priority_queue<Entry, std::vector<Entry>, std::greater<Entry>> heap;
    distance[source] = 0;
    heap.emplace(0, source);
    while (!heap.empty()) {
        const auto [d, u] = heap.top();
        heap.pop();
        if (d != distance[u]) continue; // Ignore an outdated heap entry.
        for (const auto& [v, w] : graph[u]) {
            if (d + w < distance[v]) {
                distance[v] = d + w;
                parent[v] = u;
                heap.emplace(distance[v], v);
            }
        }
    }
    // Parent pointers describe the paths without printing O(V^2) path data.
    std::cout << "Vertex Distance Parent\n";
    for (int v = 0; v < n; ++v) {
        std::cout << v << ' ';
        if (distance[v] == infinity) std::cout << "INF -\n";
        else {
            std::cout << distance[v] << ' ';
            if (parent[v] == -1) std::cout << '-';
            else std::cout << parent[v];
            std::cout << '\n';
        }
    }
}
