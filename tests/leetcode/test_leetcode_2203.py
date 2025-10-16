"""
LeetCode 2203: Minimum Weighted Subgraph With the Required Paths

Problem: Given a weighted directed graph with n nodes (0 to n-1), edges, and three
distinct nodes src1, src2, and dest, find the minimum weight of a subgraph such
that it's possible to reach dest from both src1 and src2.

Solution: Use Dijkstra's algorithm three times:
1. Find shortest paths from src1 to all nodes
2. Find shortest paths from src2 to all nodes
3. Find shortest paths from all nodes to dest (by reversing the graph)

Then for each node, calculate: dist1[node] + dist2[node] + distReverse[node]
The minimum value is our answer (this node is the meeting point).
"""

import unittest
import heapq
from typing import List, Dict, Tuple
from collections import defaultdict


class Solution:
    def minimumWeight(self, n: int, edges: List[List[int]], src1: int, src2: int, dest: int) -> int:
        """
        Find the minimum weight of a subgraph where both src1 and src2 can reach dest.

        Args:
            n: Number of nodes (0 to n-1)
            edges: List of [from, to, weight] edges
            src1: First source node
            src2: Second source node
            dest: Destination node

        Returns:
            Minimum weight or -1 if impossible
        """
        # Build adjacency lists for forward and reverse graphs
        graph = defaultdict(list)  # forward graph
        reverse_graph = defaultdict(list)  # reverse graph

        for u, v, w in edges:
            graph[u].append((v, w))
            reverse_graph[v].append((u, w))

        # Dijkstra's algorithm
        def dijkstra(start: int, adj_list: Dict[int, List[Tuple[int, int]]]) -> List[int]:
            """
            Run Dijkstra's algorithm from start node.

            Args:
                start: Starting node
                adj_list: Adjacency list representation of graph

            Returns:
                List of shortest distances from start to all nodes
            """
            dist = [float('inf')] * n
            dist[start] = 0
            pq = [(0, start)]  # (distance, node)

            while pq:
                d, u = heapq.heappop(pq)

                if d > dist[u]:
                    continue

                for v, w in adj_list[u]:
                    if dist[u] + w < dist[v]:
                        dist[v] = dist[u] + w
                        heapq.heappush(pq, (dist[v], v))

            return dist

        # Run Dijkstra from src1, src2, and from all nodes to dest (reverse graph)
        dist_from_src1 = dijkstra(src1, graph)
        dist_from_src2 = dijkstra(src2, graph)
        dist_to_dest = dijkstra(dest, reverse_graph)

        # Find the minimum total weight
        # The meeting point is a node where both sources can reach it,
        # and it can reach the destination
        min_weight = float('inf')

        for node in range(n):
            total = dist_from_src1[node] + dist_from_src2[node] + dist_to_dest[node]
            min_weight = min(min_weight, total)

        return min_weight if min_weight != float('inf') else -1


class TestLeetCode2203(unittest.TestCase):
    """Test cases for LeetCode 2203: Minimum Weighted Subgraph With the Required Paths"""

    def setUp(self):
        """Set up test fixture"""
        self.solution = Solution()

    def test_example1(self):
        """
        Test Example 1 from LeetCode

        Input: n = 6, edges = [[0,2,2],[0,5,6],[1,0,3],[1,4,5],[2,1,1],[2,3,3],[2,3,4],[3,4,2],[4,5,1]],
               src1 = 0, src2 = 1, dest = 5
        Output: 9

        Explanation: The optimal path uses edges [1,0,3], [0,2,2], [2,3,3], [3,4,2], [4,5,1]
        or [1,0,3], [0,5,6] with total weight 9.
        """
        n = 6
        edges = [[0,2,2],[0,5,6],[1,0,3],[1,4,5],[2,1,1],[2,3,3],[2,3,4],[3,4,2],[4,5,1]]
        src1 = 0
        src2 = 1
        dest = 5

        result = self.solution.minimumWeight(n, edges, src1, src2, dest)
        self.assertEqual(result, 9)

    def test_example2(self):
        """
        Test Example 2 from LeetCode

        Input: n = 3, edges = [[0,1,1],[2,1,1]], src1 = 0, src2 = 1, dest = 2
        Output: -1

        Explanation: No path exists from node 1 to node 2, so it's impossible.
        """
        n = 3
        edges = [[0,1,1],[2,1,1]]
        src1 = 0
        src2 = 1
        dest = 2

        result = self.solution.minimumWeight(n, edges, src1, src2, dest)
        self.assertEqual(result, -1)

    def test_simple_meeting_point(self):
        """
        Test a simple case where paths meet at a common node.

        Graph:
        src1(0) --2--> meeting(2) --1--> dest(3)
                        ^
                        |
        src2(1) -------3

        Minimum weight = 2 + 3 + 1 = 6
        """
        n = 4
        edges = [[0,2,2],[1,2,3],[2,3,1]]
        src1 = 0
        src2 = 1
        dest = 3

        result = self.solution.minimumWeight(n, edges, src1, src2, dest)
        self.assertEqual(result, 6)

    def test_direct_paths(self):
        """
        Test where both sources have direct paths to destination.

        Graph:
        src1(0) --5--> dest(2)
        src2(1) --3--> dest(2)

        Minimum weight = 5 + 3 + 0 = 8 (meeting at dest)
        """
        n = 3
        edges = [[0,2,5],[1,2,3]]
        src1 = 0
        src2 = 1
        dest = 2

        result = self.solution.minimumWeight(n, edges, src1, src2, dest)
        self.assertEqual(result, 8)

    def test_src1_unreachable(self):
        """
        Test where src1 cannot reach dest.

        Graph:
        src1(0)  (isolated)
        src2(1) --1--> dest(2)

        Should return -1
        """
        n = 3
        edges = [[1,2,1]]
        src1 = 0
        src2 = 1
        dest = 2

        result = self.solution.minimumWeight(n, edges, src1, src2, dest)
        self.assertEqual(result, -1)

    def test_src2_unreachable(self):
        """
        Test where src2 cannot reach dest.

        Graph:
        src1(0) --1--> dest(2)
        src2(1)  (isolated)

        Should return -1
        """
        n = 3
        edges = [[0,2,1]]
        src1 = 0
        src2 = 1
        dest = 2

        result = self.solution.minimumWeight(n, edges, src1, src2, dest)
        self.assertEqual(result, -1)

    def test_complex_graph(self):
        """
        Test a more complex graph with multiple possible paths.

        Graph with multiple paths and meeting points.
        """
        n = 5
        edges = [
            [0,2,3],  # src1 -> 2
            [1,2,2],  # src2 -> 2
            [2,3,1],  # 2 -> 3
            [3,4,1],  # 3 -> dest
            [0,3,5],  # src1 -> 3 (alternative)
            [1,3,4],  # src2 -> 3 (alternative)
        ]
        src1 = 0
        src2 = 1
        dest = 4

        # Best path: src1->2 (3) + src2->2 (2) + 2->3->dest (1+1) = 7
        result = self.solution.minimumWeight(n, edges, src1, src2, dest)
        self.assertEqual(result, 7)

    def test_same_source_and_dest(self):
        """
        Test edge case where one source is the meeting point.

        Graph:
        src1(0) = meeting point
        src2(1) --2--> src1(0) --3--> dest(2)

        Minimum: 0 + 2 + 3 = 5
        """
        n = 3
        edges = [[1,0,2],[0,2,3]]
        src1 = 0
        src2 = 1
        dest = 2

        result = self.solution.minimumWeight(n, edges, src1, src2, dest)
        self.assertEqual(result, 5)

    def test_large_weights(self):
        """
        Test with larger weight values.
        """
        n = 4
        edges = [[0,2,1000],[1,2,2000],[2,3,500]]
        src1 = 0
        src2 = 1
        dest = 3

        result = self.solution.minimumWeight(n, edges, src1, src2, dest)
        self.assertEqual(result, 3500)

    def test_single_edge_path(self):
        """
        Test minimal graph with single edges.
        """
        n = 4
        edges = [[0,3,1],[1,3,1],[3,2,1]]
        src1 = 0
        src2 = 1
        dest = 2

        # Both reach node 3, then go to dest
        # 1 + 1 + 1 = 3
        result = self.solution.minimumWeight(n, edges, src1, src2, dest)
        self.assertEqual(result, 3)


if __name__ == '__main__':
    unittest.main()
