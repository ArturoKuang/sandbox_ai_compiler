"""
Unit tests for Dijkstra's algorithm implementation in SimpleLang.
"""

import unittest
import subprocess
import os


class TestDijkstraAlgorithm(unittest.TestCase):
    """Test cases for Dijkstra's shortest path algorithm."""

    def compile_and_execute(self, source: str) -> str:
        """Helper method to compile and execute SimpleLang code."""
        # Write source to temporary file
        temp_file = "temp_test.sl"
        with open(temp_file, 'w') as f:
            f.write(source)

        try:
            # Run the compiler with --run flag
            result = subprocess.run(
                ['python', 'simplelang.py', temp_file, '--run'],
                capture_output=True,
                text=True,
                timeout=5
            )

            # Check if compilation was successful
            if result.returncode != 0:
                raise RuntimeError(f"Compilation failed: {result.stderr}")

            # Extract the output (after the "Running generated code:" line)
            lines = result.stdout.split('\n')
            output_lines = []
            capture = False
            for line in lines:
                if "Running generated code:" in line or "----" in line:
                    capture = True
                    continue
                if capture and line.strip():
                    output_lines.append(line.strip())

            return '\n'.join(output_lines)

        finally:
            # Clean up temporary files
            if os.path.exists(temp_file):
                os.remove(temp_file)
            temp_py = temp_file.replace('.sl', '.py')
            if os.path.exists(temp_py):
                os.remove(temp_py)

    def test_dijkstra_simple_graph(self):
        """Test Dijkstra's algorithm on a simple graph."""
        source = """
function dijkstra(int graph, int n, int src, int dest) {
    int dist = [999999, 999999, 999999, 999999];
    int visited = [0, 0, 0, 0];

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

int n = 4;
int graph = [
    0, 1, 4, 0,
    0, 0, 2, 5,
    0, 0, 0, 1,
    0, 0, 0, 0
];

int result = dijkstra(graph, n, 0, 3);
print(result);
"""
        output = self.compile_and_execute(source)
        self.assertEqual(output, "4", "Shortest path from 0 to 3 should be 4")

    def test_dijkstra_no_path(self):
        """Test Dijkstra's algorithm when no path exists."""
        source = """
function dijkstra(int graph, int n, int src, int dest) {
    int dist = [999999, 999999, 999999, 999999];
    int visited = [0, 0, 0, 0];

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

int n = 4;
int graph = [
    0, 1, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 1,
    0, 0, 0, 0
];

int result = dijkstra(graph, n, 0, 3);
print(result);
"""
        output = self.compile_and_execute(source)
        self.assertEqual(output, "999999", "Should return infinity when no path exists")

    def test_dijkstra_same_node(self):
        """Test Dijkstra's algorithm when source equals destination."""
        source = """
function dijkstra(int graph, int n, int src, int dest) {
    int dist = [999999, 999999, 999999, 999999];
    int visited = [0, 0, 0, 0];

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

int n = 4;
int graph = [
    0, 1, 4, 0,
    0, 0, 2, 5,
    0, 0, 0, 1,
    0, 0, 0, 0
];

int result = dijkstra(graph, n, 2, 2);
print(result);
"""
        output = self.compile_and_execute(source)
        self.assertEqual(output, "0", "Distance from node to itself should be 0")

    def test_dijkstra_complex_graph(self):
        """Test Dijkstra's algorithm on the original 6-node graph."""
        source = """
function dijkstra(int graph, int n, int src, int dest) {
    int dist = [999999, 999999, 999999, 999999, 999999, 999999];
    int visited = [0, 0, 0, 0, 0, 0];

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

int n = 6;
int graph = [
    0, 7, 9, 0, 0, 14,
    7, 0, 10, 15, 0, 0,
    9, 10, 0, 11, 0, 2,
    0, 15, 11, 0, 6, 0,
    0, 0, 0, 6, 0, 9,
    14, 0, 2, 0, 9, 0
];

int result = dijkstra(graph, n, 0, 5);
print(result);
"""
        output = self.compile_and_execute(source)
        self.assertEqual(output, "11", "Shortest path from 0 to 5 should be 11")


if __name__ == '__main__':
    unittest.main()
