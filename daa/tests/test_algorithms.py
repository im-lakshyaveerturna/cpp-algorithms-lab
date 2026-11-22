#!/usr/bin/env python3
"""Compile standalone programs, then check samples, edge cases and random oracles.

Only Python's standard library and a C++17 compiler are needed.
Use CXX=clang++ or CXX=g++ to choose a compiler.
"""
import collections
import itertools
import os
from pathlib import Path
import random
import re
import shlex
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
RNG = random.Random(2026)
EXECUTABLES = {}
CHECKS = 0
TIMEOUT_SECONDS = int(os.environ.get("DAA_PROGRAM_TIMEOUT_SECONDS", "30"))


def run(name, data, valid=True):
    global CHECKS
    result = subprocess.run([str(EXECUTABLES[name])], input=data, text=True,
                            capture_output=True, timeout=TIMEOUT_SECONDS)
    CHECKS += 1
    if valid:
        assert result.returncode == 0, (name, data, result.stderr)
        assert not result.stderr, (name, result.stderr)
    else:
        assert result.returncode != 0 and "Error:" in result.stderr, (name, data, result)
    return result.stdout


def ids(line):
    text = line.split(":", 1)[1].strip()
    return [] if text == "none" else list(map(int, text.split()))


def check_strassen():
    for n in [1, 2, 3, 4, 5, 7, 8, 9, 16, 17]:
        for _ in range(3):
            a = [[RNG.randint(-20, 20) for _ in range(n)] for _ in range(n)]
            b = [[RNG.randint(-20, 20) for _ in range(n)] for _ in range(n)]
            data = str(n) + "\n" + "\n".join(" ".join(map(str, row)) for row in a + b) + "\n"
            actual = [list(map(int, row.split())) for row in run("01_strassen", data).splitlines()[1:]]
            expected = [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)]
                        for i in range(n)]
            assert actual == expected, (n, actual, expected)
    n = 128
    data = str(n) + "\n" + ("10000 " * (2 * n * n)) + "\n"
    actual = list(map(int, run("01_strassen", data).split(":", 1)[1].split()))
    assert actual == [n * 10000**2] * (n * n)


def check_traversals():
    compiler = shlex.split(os.environ.get("CXX", "c++"))
    flags = ["-std=c++17", "-O2", "-Wall", "-Wextra", "-Wpedantic", "-Werror"]
    flags += shlex.split(os.environ.get("CXXFLAGS", ""))
    for kind, stem in [("bfs", "02_bfs"), ("dfs", "03_dfs")]:
        source = ROOT / "programs" / f"{stem}.cpp"
        # Test the actual reference-style helpers with varied graphs, without
        # changing the built-in demonstration or its console format.
        driver = '#define main reference_style_demo_main\n#include "' + str(source) + '"\n#undef main\n'
        driver += "int main() { int n, m, start; std::cin >> n >> m; "
        driver += "std::vector<std::vector<int>> edges(m, std::vector<int>(2)); "
        driver += "for (auto& e : edges) std::cin >> e[0] >> e[1]; std::cin >> start; "
        if kind == "bfs":
            driver += "auto graph = adjList(n - 1, edges); std::vector<int> result; "
            driver += "if (n > 0) result = bfs(graph, start); "
            driver += "if (findSize(edges) != "
        else:
            driver += "auto graph = adjList(n, edges); std::vector<int> result; "
            driver += "std::vector<bool> visited(n, false); if (n > 0) dfs(graph, start, result, visited); "
            driver += "if (findSize(edges) - 1 != "
        driver += "[&]() { int maximum = -1; for (auto& e : edges) "
        driver += "for (int v : e) if (v > maximum) maximum = v; return maximum; }()) return 2; "
        driver += "for (int v : result) std::cout << v << ' '; return 0; }\n"
        harness = BUILD / f"{kind}_helper.cpp"
        harness.write_text(driver)
        target = BUILD / f"{kind}_helper"
        subprocess.run(compiler + flags + [str(harness), "-o", str(target)], check=True)
        EXECUTABLES[f"{kind}_helper"] = target

        # Exercise the real main after changing only its built-in edge list.
        # Its former fixed-size output loop read past the traversal on a
        # disconnected graph; empty demos also used to visit absent vertex 0.
        original = source.read_text()
        for label, edges, expected in [
                ("disconnected", "{{0,1}, {2,3}}", [0, 1]),
                ("empty", "{}", [])]:
            modified, count = re.subn(
                r"(?m)^\tvector<vector<int>> edges = .+ ;$",
                "\tvector<vector<int>> edges = " + edges + " ;", original)
            assert count == 1
            variant = BUILD / f"{kind}_{label}.cpp"
            variant.write_text(modified)
            executable = BUILD / f"{kind}_{label}"
            subprocess.run(compiler + flags + [str(variant), "-o", str(executable)], check=True)
            EXECUTABLES[f"{kind}_{label}"] = executable
            output = run(f"{kind}_{label}", "")
            assert list(map(int, output.rsplit(": ", 1)[1].split())) == expected

    # Insertion order and source-component-only traversal match upstream.
    generator = random.Random(2026)
    cases = [(0, [], 0), (1, [], 0), (4, [(0, 1), (2, 3)], 0),
             (5, [(0, 2), (0, 3), (0, 1), (2, 4)], 0),
             (200, [(i, i + 1) for i in range(199)], 0)]
    for _ in range(50):
        n = generator.randint(1, 12)
        edges = [(u, v) for u in range(n) for v in range(u, n) if generator.random() < 0.15]
        if edges:
            edges.append(edges[0])
        generator.shuffle(edges)
        cases.append((n, edges, generator.randrange(n)))
    for n, edges, start in cases:
        graph = [[] for _ in range(n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        data = f"{n} {len(edges)}\n" + "".join(f"{u} {v}\n" for u, v in edges) + f"{start}\n"
        for kind in ["bfs", "dfs"]:
            seen, order = set(), []

            def visit(u):
                seen.add(u)
                order.append(u)
                for v in graph[u]:
                    if v not in seen:
                        visit(v)

            if n and kind == "dfs":
                visit(start)
            elif n:
                pending = collections.deque([start])
                seen.add(start)
                while pending:
                    u = pending.popleft()
                    order.append(u)
                    for v in graph[u]:
                        if v not in seen:
                            seen.add(v)
                            pending.append(v)
            actual = list(map(int, run(f"{kind}_helper", data).split()))
            assert actual == order, (kind, data, actual, order)


def check_prim():
    for _ in range(60):
        n = RNG.randint(1, 10)
        edges = [(u, v, RNG.randint(-10, 20)) for u in range(n) for v in range(u, n)
                 if RNG.random() < 0.25]
        if edges:
            u, v, w = edges[0]
            edges.append((u, v, w - 1))
        data = f"{n} {len(edges)}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges)
        # Independent Kruskal oracle, including disconnected graphs.
        parent = list(range(n))

        def find(v):
            while parent[v] != v:
                v = parent[v]
            return v

        expected, count = 0, 0
        for u, v, w in sorted(edges, key=lambda e: e[2]):
            a, b = find(u), find(v)
            if a != b:
                parent[a] = b
                expected += w
                count += 1
        output = run("04_prim", data).splitlines()
        assert int(output[-2].split(":")[1]) == expected
        assert int(output[-1].split(":")[1]) == n - count
        edge_lines = output[1:-2] if n - count == 1 else output[2:-2]
        selected = [tuple(map(int, line.split())) for line in edge_lines]
        assert len(selected) == count and sum(w for _, _, w in selected) == expected
        parent = list(range(n))
        for u, v, w in selected:
            assert (u, v, w) in edges or (v, u, w) in edges
            a, b = find(u), find(v)
            assert a != b
            parent[a] = b


def check_dijkstra():
    for _ in range(60):
        n, directed = RNG.randint(1, 10), RNG.randrange(2)
        edges = [(u, v, RNG.randint(0, 20)) for u in range(n) for v in range(n)
                 if RNG.random() < 0.12]
        source = RNG.randrange(n)
        infinity = float("inf")
        distance = [[infinity] * n for _ in range(n)]
        for v in range(n):
            distance[v][v] = 0
        for u, v, w in edges:
            distance[u][v] = min(distance[u][v], w)
            if not directed:
                distance[v][u] = min(distance[v][u], w)
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])
        data = f"{n} {len(edges)} {directed}\n"
        data += "".join(f"{u} {v} {w}\n" for u, v, w in edges) + f"{source}\n"
        rows = [line.split() for line in run("05_dijkstra", data).splitlines()[1:]]
        assert len(rows) == n
        for v, row in enumerate(rows):
            assert int(row[0]) == v
            actual = infinity if row[1] == "INF" else int(row[1])
            assert actual == distance[source][v], (data, v, rows)
            if actual == infinity or v == source:
                assert row[2] == "-"
            else:
                p = int(row[2])
                candidates = [w for u, end, w in edges if (u, end) == (p, v) or
                              (not directed and (u, end) == (v, p))]
                assert candidates and distance[source][p] + min(candidates) == actual
                seen, cursor = set(), v
                while cursor != source:
                    assert cursor not in seen
                    seen.add(cursor)
                    cursor = int(rows[cursor][2])


def check_intervals():
    for _ in range(70):
        n = RNG.randint(0, 10)
        jobs = []
        for _ in range(n):
            start = RNG.randint(0, 12)
            jobs.append((start, start + RNG.randint(1, 5), RNG.randint(-5, 20)))
        expected = 0
        for mask in range(1 << n):
            subset = sorted(jobs[i] for i in range(n) if mask & (1 << i))
            if all(a[1] <= b[0] for a, b in zip(subset, subset[1:])):
                expected = max(expected, sum(job[2] for job in subset))
        data = f"{n}\n" + "".join(f"{s} {f} {p}\n" for s, f, p in jobs)
        output = run("06_weighted_interval_scheduling", data).splitlines()
        assert int(output[0].split(":")[1]) == expected
        selected = ids(output[1])
        assert len(set(selected)) == len(selected) and all(1 <= i <= n for i in selected)
        chosen = [jobs[i - 1] for i in selected]
        assert sum(job[2] for job in chosen) == expected
        assert all(a[1] <= b[0] for a, b in zip(chosen, chosen[1:]))


def check_knapsack():
    for _ in range(70):
        n, capacity = RNG.randint(0, 10), RNG.randint(0, 20)
        items = [(RNG.randint(0, 12), RNG.randint(-5, 20)) for _ in range(n)]
        expected = 0
        for subset in itertools.product([False, True], repeat=n):
            weight = sum(w for (w, _), take in zip(items, subset) if take)
            value = sum(v for (_, v), take in zip(items, subset) if take)
            if weight <= capacity:
                expected = max(expected, value)
        data = f"{n} {capacity}\n" + "".join(f"{w} {v}\n" for w, v in items)
        output = run("13_zero_one_knapsack", data).splitlines()
        assert int(output[0].split(":")[1]) == expected
        selected = ids(output[1])
        assert len(set(selected)) == len(selected) and all(1 <= i <= n for i in selected)
        assert sum(items[i - 1][1] for i in selected) == expected
        total = sum(items[i - 1][0] for i in selected)
        assert total <= capacity and int(output[2].split(":")[1]) == total
    assert "Maximum value: 7\n" in run("13_zero_one_knapsack", "2 0\n0 7\n0 -2\n")


def check_invalid_inputs():
    cases = {
        "01_strassen": ["0\n", "129\n", "1\n10001\n2\n", "1\n2\n"],
        "04_prim": ["0 0\n", "2 1\n0 2 3\n", "2 1\n0 1 1000000001\n"],
        "05_dijkstra": ["2 1 0\n0 1 -1\n0\n", "1 0 2\n0\n", "1 0 0\n1\n"],
        "06_weighted_interval_scheduling": ["-1\n", "1\n3 3 5\n", "1\n4 2 5\n"],
        "13_zero_one_knapsack": ["2 -1\n", "1 3\n-1 5\n", "201 0\n"],
    }
    for name, inputs in cases.items():
        for data in ["", "not-a-number\n"] + inputs:
            run(name, data, valid=False)


def main():
    BUILD.mkdir(exist_ok=True)
    compiler = shlex.split(os.environ.get("CXX", "c++"))
    extra_flags = shlex.split(os.environ.get("CXXFLAGS", ""))
    for source in sorted((ROOT / "programs").glob("*.cpp")):
        target = BUILD / source.stem
        subprocess.run(compiler + ["-std=c++17", "-O2", "-Wall", "-Wextra", "-Wpedantic",
                                  "-Werror"] + extra_flags + [str(source), "-o", str(target)], check=True)
        EXECUTABLES[source.stem] = target
    assert len(EXECUTABLES) == 7
    for name in EXECUTABLES:
        expected = (ROOT / "samples" / f"{name}.out").read_text()
        assert run(name, (ROOT / "samples" / f"{name}.in").read_text()) == expected, name
    for check in [check_strassen, check_traversals, check_prim, check_dijkstra,
                  check_intervals, check_knapsack, check_invalid_inputs]:
        check()
        print(f"PASS: {check.__name__}", flush=True)
    print(f"All seven programs compiled; {CHECKS} program runs passed.")


if __name__ == "__main__":
    main()
