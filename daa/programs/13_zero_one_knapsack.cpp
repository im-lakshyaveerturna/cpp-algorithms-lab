// Experiment 13: 0/1 knapsack using a two-dimensional DP table.
#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    int n, capacity;
    if (!(std::cin >> n >> capacity) || n < 0 || n > 200 || capacity < 0 || capacity > 10000) {
        std::cerr << "Error: require 0..200 items and capacity in [0, 10000].\n";
        return 1;
    }
    std::vector<int> weight(n + 1);
    std::vector<long long> value(n + 1);
    for (int i = 1; i <= n; ++i) {
        if (!(std::cin >> weight[i] >> value[i]) || weight[i] < 0 || weight[i] > 1000000000 ||
            value[i] < -1000000000LL || value[i] > 1000000000LL) {
            std::cerr << "Error: require weight in [0, 10^9] and value in [-10^9, 10^9].\n";
            return 1;
        }
    }
    // best[i][w] = maximum value using only the first i items, capacity w.
    std::vector<std::vector<long long>> best(n + 1, std::vector<long long>(capacity + 1));
    for (int i = 1; i <= n; ++i) {
        for (int w = 0; w <= capacity; ++w) {
            best[i][w] = best[i - 1][w];
            if (weight[i] <= w)
                best[i][w] = std::max(best[i][w], value[i] + best[i - 1][w - weight[i]]);
        }
    }
    std::vector<int> chosen;
    int remaining = capacity;
    long long total_weight = 0;
    for (int i = n; i > 0; --i) {
        if (best[i][remaining] > best[i - 1][remaining]) {
            chosen.push_back(i);
            remaining -= weight[i];
            total_weight += weight[i];
        }
    }
    std::reverse(chosen.begin(), chosen.end());
    std::cout << "Maximum value: " << best[n][capacity] << "\nSelected item IDs:";
    if (chosen.empty()) std::cout << " none";
    for (int id : chosen) std::cout << ' ' << id;
    std::cout << "\nTotal weight: " << total_weight << '\n';
}
