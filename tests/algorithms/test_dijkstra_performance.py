#!/usr/bin/env python3
"""
Performance test for Dijkstra's algorithm in SimpleLang.
Tests with the largest practical graph size given SimpleLang's constraints.
"""

import subprocess
import time
import sys
import os

def generate_dijkstra_code(n, use_priority_queue=True):
    """Generate SimpleLang code for Dijkstra with n nodes."""

    if use_priority_queue:
        pq_functions = """
function pq_swap(int priorities, int values, int i, int j) {
    int tempPriority = priorities[i];
    priorities[i] = priorities[j];
    priorities[j] = tempPriority;

    int tempValue = values[i];
    values[i] = values[j];
    values[j] = tempValue;

    return 0;
}

function pq_heapify_up(int priorities, int values, int idx) {
    while (idx > 0) {
        int parent = (idx - 1) / 2;

        if (priorities[idx] < priorities[parent]) {
            int dummy = pq_swap(priorities, values, idx, parent);
            idx = parent;
        } else {
            return 0;
        }
    }
    return 0;
}

function pq_heapify_down(int priorities, int values, int size, int idx) {
    while (1 == 1) {
        int left = 2 * idx + 1;
        int right = 2 * idx + 2;
        int smallest = idx;

        if (left < size && priorities[left] < priorities[smallest]) {
            smallest = left;
        }

        if (right < size && priorities[right] < priorities[smallest]) {
            smallest = right;
        }

        if (smallest != idx) {
            int dummy = pq_swap(priorities, values, idx, smallest);
            idx = smallest;
        } else {
            return 0;
        }
    }
    return 0;
}

function pq_insert(int priorities, int values, int size, int priority, int value) {
    priorities[size] = priority;
    values[size] = value;

    int dummy = pq_heapify_up(priorities, values, size);

    return size + 1;
}

function pq_extract_min_value(int priorities, int values, int size) {
    if (size == 0) {
        return -1;
    }

    int minValue = values[0];

    priorities[0] = priorities[size - 1];
    values[0] = values[size - 1];

    int dummy = pq_heapify_down(priorities, values, size - 1, 0);

    return minValue;
}

function pq_is_empty(int size) {
    if (size == 0) {
        return 1;
    }
    return 0;
}

function dijkstra(int graph, int n, int src, int dest) {
    int maxNodes = """ + str(n * 2) + """;
    int pqPriorities = [""" + ", ".join(["999999"] * (n * 2)) + """];
    int pqValues = [""" + ", ".join(["0"] * (n * 2)) + """];
    int pqSize = 0;

    int dist = [""" + ", ".join(["999999"] * n) + """];
    int visited = [""" + ", ".join(["0"] * n) + """];
    int inQueue = [""" + ", ".join(["0"] * n) + """];

    dist[src] = 0;
    pqSize = pq_insert(pqPriorities, pqValues, pqSize, 0, src);
    inQueue[src] = 1;

    while (pq_is_empty(pqSize) == 0) {
        int u = pq_extract_min_value(pqPriorities, pqValues, pqSize);
        pqSize = pqSize - 1;
        inQueue[u] = 0;

        if (visited[u] == 1) {
            int dummy = 0;
        } else {
            visited[u] = 1;

            int v = 0;
            while (v < n) {
                int weight = graph[u * n + v];
                if (visited[v] == 0 && weight != 0 && dist[u] != 999999) {
                    int newDist = dist[u] + weight;
                    if (newDist < dist[v]) {
                        dist[v] = newDist;
                        pqSize = pq_insert(pqPriorities, pqValues, pqSize, newDist, v);
                        inQueue[v] = 1;
                    }
                }
                v = v + 1;
            }
        }
    }

    return dist[dest];
}
"""
    else:
        pq_functions = """
function dijkstra(int graph, int n, int src, int dest) {
    int dist = [""" + ", ".join(["999999"] * n) + """];
    int visited = [""" + ", ".join(["0"] * n) + """];

    dist[src] = 0;

    int count = 0;
    while (count < n) {
        int minDist = 999999;
        int u = -1;

        int i = 0;
        while (i < n) {
            if (visited[i] == 0 && dist[i] < minDist) {
                minDist = dist[i];
                u = i;
            }
            i = i + 1;
        }

        if (u == -1) {
            return dist[dest];
        }

        visited[u] = 1;

        int v = 0;
        while (v < n) {
            int weight = graph[u * n + v];
            if (visited[v] == 0 && weight != 0 && dist[u] != 999999) {
                int newDist = dist[u] + weight;
                if (newDist < dist[v]) {
                    dist[v] = newDist;
                }
            }
            v = v + 1;
        }

        count = count + 1;
    }

    return dist[dest];
}
"""

    # Generate a graph with edges forming a chain and some cross-edges
    # This creates a graph where we need to explore multiple paths
    graph = []
    for i in range(n):
        for j in range(n):
            if j == i + 1:  # Chain edge
                graph.append("1")
            elif j == i + 2 and i % 3 == 0:  # Skip edge every 3 nodes
                graph.append("2")
            elif i == j + 1 and j % 5 == 0:  # Backward edge every 5 nodes
                graph.append("3")
            else:
                graph.append("0")

    graph_str = ", ".join(graph)

    code = pq_functions + f"""
int n = {n};
int graph = [{graph_str}];

int result = dijkstra(graph, n, 0, {n-1});
print(result);
"""
    return code

def run_performance_test(n, use_priority_queue=True):
    """Run performance test with n nodes."""
    print(f"\n{'='*70}")
    impl_type = "Priority Queue" if use_priority_queue else "Linear Search"
    print(f"Testing Dijkstra ({impl_type}) with {n} nodes")
    print(f"{'='*70}")

    code = generate_dijkstra_code(n, use_priority_queue)

    with open('perf_test.sl', 'w') as f:
        f.write(code)

    try:
        # Compile
        print("Compiling SimpleLang code...")
        compile_start = time.time()
        compile_result = subprocess.run(
            ['python3', 'simplelang.py', 'perf_test.sl'],
            capture_output=True,
            text=True,
            timeout=30
        )
        compile_time = time.time() - compile_start

        if compile_result.returncode != 0:
            print(f"❌ Compilation failed: {compile_result.stderr}")
            return None

        print(f"✓ Compilation time: {compile_time:.3f}s")

        # Run
        print("Running compiled code...")
        run_start = time.time()
        run_result = subprocess.run(
            ['python3', 'perf_test.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        run_time = time.time() - run_start

        if run_result.returncode != 0:
            print(f"❌ Execution failed: {run_result.stderr}")
            return None

        result = run_result.stdout.strip()
        print(f"✓ Execution time: {run_time:.3f}s")
        print(f"✓ Result (shortest path): {result}")
        print(f"✓ Total time: {compile_time + run_time:.3f}s")

        return {
            'n': n,
            'compile_time': compile_time,
            'run_time': run_time,
            'total_time': compile_time + run_time,
            'result': result,
            'use_pq': use_priority_queue
        }

    except subprocess.TimeoutExpired:
        print(f"❌ Test timed out (>60s)")
        return None
    finally:
        if os.path.exists('perf_test.sl'):
            os.remove('perf_test.sl')
        if os.path.exists('perf_test.py'):
            os.remove('perf_test.py')

def main():
    """Run performance tests with increasing graph sizes."""
    print("=" * 70)
    print("SimpleLang Dijkstra Performance Benchmark")
    print("=" * 70)
    print("\nThis benchmark compares Priority Queue vs Linear Search implementations")
    print("Testing with progressively larger graphs...\n")

    # Test sizes - SimpleLang has practical limits due to array initialization
    test_sizes = [10, 20, 30, 40, 50]

    results = []

    for n in test_sizes:
        # Test with priority queue
        result_pq = run_performance_test(n, use_priority_queue=True)
        if result_pq:
            results.append(result_pq)

        # Test without priority queue (linear search)
        result_linear = run_performance_test(n, use_priority_queue=False)
        if result_linear:
            results.append(result_linear)

        # Compare
        if result_pq and result_linear:
            speedup = result_linear['run_time'] / result_pq['run_time']
            print(f"\n📊 Speedup (PQ vs Linear): {speedup:.2f}x")

    # Summary
    print("\n" + "=" * 70)
    print("PERFORMANCE SUMMARY")
    print("=" * 70)
    print(f"{'Nodes':<10} {'Type':<15} {'Compile':<12} {'Run':<12} {'Total':<12}")
    print("-" * 70)

    for r in results:
        impl_type = "PQ" if r['use_pq'] else "Linear"
        print(f"{r['n']:<10} {impl_type:<15} {r['compile_time']:<12.3f} {r['run_time']:<12.3f} {r['total_time']:<12.3f}")

    print("\n" + "=" * 70)
    print("Note: SimpleLang has practical limits due to static array initialization.")
    print("For real-world scale (100M nodes), use native implementations.")
    print("=" * 70)

if __name__ == "__main__":
    main()
