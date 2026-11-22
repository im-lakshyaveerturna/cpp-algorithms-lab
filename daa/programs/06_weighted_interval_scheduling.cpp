// Experiment 6: Weighted interval scheduling using dynamic programming.
#include <algorithm>
#include <iostream>
#include <tuple>
#include <vector>

struct Job {
    long long start, finish, profit;
    int id;
};

int main() {
    int n;
    if (!(std::cin >> n) || n < 0 || n > 100000) {
        std::cerr << "Error: number of jobs must be in [0, 100000].\n";
        return 1;
    }
    std::vector<Job> jobs(n);
    for (int i = 0; i < n; ++i) {
        auto& job = jobs[i];
        job.id = i + 1;
        if (!(std::cin >> job.start >> job.finish >> job.profit) || job.start < 0 ||
            job.finish <= job.start || job.finish > 1000000000LL ||
            job.profit < -1000000000LL || job.profit > 1000000000LL) {
            std::cerr << "Error: require 0 <= start < finish <= 10^9 and profit in [-10^9, 10^9].\n";
            return 1;
        }
    }
    std::sort(jobs.begin(), jobs.end(), [](const Job& a, const Job& b) {
        return std::tie(a.finish, a.start, a.id) < std::tie(b.finish, b.start, b.id);
    });
    std::vector<long long> finish(n);
    for (int i = 0; i < n; ++i) finish[i] = jobs[i].finish;
    std::vector<int> compatible(n);
    std::vector<long long> best(n + 1, 0);
    for (int i = 0; i < n; ++i) {
        // Number of earlier jobs ending at or before this job starts.
        compatible[i] = static_cast<int>(std::upper_bound(finish.begin(), finish.begin() + i,
                                                         jobs[i].start) - finish.begin());
        // best[i+1] = max(skip job i, take job i + compatible optimum).
        best[i + 1] = std::max(best[i], jobs[i].profit + best[compatible[i]]);
    }
    std::vector<int> chosen;
    for (int i = n; i > 0;) {
        if (jobs[i - 1].profit + best[compatible[i - 1]] > best[i - 1]) {
            chosen.push_back(jobs[i - 1].id);
            i = compatible[i - 1];
        } else --i; // On ties, prefer the solution that skips this job.
    }
    std::reverse(chosen.begin(), chosen.end());
    std::cout << "Maximum profit: " << best[n] << "\nSelected job IDs:";
    if (chosen.empty()) std::cout << " none";
    for (int id : chosen) std::cout << ' ' << id;
    std::cout << '\n';
}
