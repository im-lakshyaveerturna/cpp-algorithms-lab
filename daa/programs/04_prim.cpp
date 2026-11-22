// Experiment 4: Prim's greedy algorithm for a minimum spanning tree.
#include <functional>
#include <iostream>
#include <queue>
#include <tuple>
#include <utility>
#include <vector>

int main() {
    int n, m;
    if (!(std::cin >> n >> m) || n < 1 || n > 100000 || m < 0 || m > 200000) {
        std::cerr << "Error: require 1..100000 vertices and 0..200000 edges.\n";
        return 1;
    }
    std::vector<std::vector<std::pair<int, long long>>> graph(n);
    for (int i = 0; i < m; ++i) {
        int u, v;
        long long w;
        if (!(std::cin >> u >> v >> w) || u < 0 || u >= n || v < 0 || v >= n ||
            w < -1000000000LL || w > 1000000000LL) {
            std::cerr << "Error: invalid vertex or weight outside [-10^9, 10^9].\n";
            return 1;
        }
        graph[u].emplace_back(v, w);
        graph[v].emplace_back(u, w);
    }
    // Candidate = (edge weight, destination, parent).
    using Candidate = std::tuple<long long, int, int>;
    std::priority_queue<Candidate, std::vector<Candidate>, std::greater<Candidate>> heap;
    std::vector<bool> included(n, false);
    std::vector<std::tuple<int, int, long long>> selected;
    long long total = 0;
    int components = 0;
    for (int root = 0; root < n; ++root) {
        if (included[root]) continue;
        ++components;
        heap.emplace(0, root, -1);
        while (!heap.empty()) {
            const auto [weight, u, parent] = heap.top();
            heap.pop();
            if (included[u]) continue;
            included[u] = true;
            total += weight;
            if (parent != -1) selected.emplace_back(parent, u, weight);
            for (const auto& [v, w] : graph[u])
                if (!included[v]) heap.emplace(w, v, u);
        }
    }
    if (components == 1) std::cout << "Minimum spanning tree edges (u v weight):\n";
    else std::cout << "Graph is disconnected; no spanning tree exists.\n"
                   << "Minimum spanning forest edges (u v weight):\n";
    for (const auto& [u, v, w] : selected) std::cout << u << ' ' << v << ' ' << w << '\n';
    std::cout << "Total weight: " << total << "\nComponents: " << components << '\n';
}
