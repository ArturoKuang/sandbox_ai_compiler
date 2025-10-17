"""
Unit tests for A* pathfinding algorithm implementation in SimpleLang.
"""

import unittest
import subprocess
import os


class TestAStarAlgorithm(unittest.TestCase):
    """Test cases for A* pathfinding algorithm."""

    def compile_and_execute(self, source: str) -> str:
        """Helper method to compile and execute SimpleLang code."""
        # Write source to temporary file
        temp_file = "temp_test.sl"
        with open(temp_file, 'w') as f:
            f.write(source)

        try:
            # Compile the file first (to avoid the runtime error during --run)
            compile_result = subprocess.run(
                ['python', 'simplelang.py', temp_file],
                capture_output=True,
                text=True,
                timeout=5
            )

            if compile_result.returncode != 0:
                raise RuntimeError(f"Compilation failed: {compile_result.stderr}")

            # Now run the generated Python file
            temp_py = temp_file.replace('.sl', '.py')
            run_result = subprocess.run(
                ['python', temp_py],
                capture_output=True,
                text=True,
                timeout=5
            )

            if run_result.returncode != 0:
                raise RuntimeError(f"Execution failed: {run_result.stderr}")

            return run_result.stdout.strip()

        finally:
            # Clean up temporary files
            if os.path.exists(temp_file):
                os.remove(temp_file)
            temp_py = temp_file.replace('.sl', '.py')
            if os.path.exists(temp_py):
                os.remove(temp_py)

    def test_astar_simple_path(self):
        """Test A* on a simple 4x4 grid with obstacles."""
        source = """
function abs(int x) {
    if (x < 0) {
        return 0 - x;
    }
    return x;
}

function manhattan(int x1, int y1, int x2, int y2) {
    int dx = abs(x2 - x1);
    int dy = abs(y2 - y1);
    return dx + dy;
}

function astar(int grid, int width, int height, int startX, int startY, int goalX, int goalY) {
    int openSet = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    int closedSet = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    int gScore = [999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999];
    int fScore = [999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999];

    int startIdx = startY * width + startX;
    int goalIdx = goalY * width + goalX;

    openSet[startIdx] = 1;
    gScore[startIdx] = 0;
    fScore[startIdx] = manhattan(startX, startY, goalX, goalY);

    int iterations = 0;
    int maxIterations = 100;

    while (iterations < maxIterations) {
        int current = -1;
        int minF = 999999;

        int i = 0;
        while (i < width * height) {
            if (openSet[i] == 1 && fScore[i] < minF) {
                minF = fScore[i];
                current = i;
            }
            i = i + 1;
        }

        if (current == -1) {
            return -1;
        }

        if (current == goalIdx) {
            return gScore[current];
        }

        openSet[current] = 0;
        closedSet[current] = 1;

        int currentX = current % width;
        int currentY = current / width;

        int dir = 0;
        while (dir < 4) {
            int neighborX = currentX;
            int neighborY = currentY;

            if (dir == 0) {
                neighborY = neighborY - 1;
            }
            if (dir == 1) {
                neighborX = neighborX + 1;
            }
            if (dir == 2) {
                neighborY = neighborY + 1;
            }
            if (dir == 3) {
                neighborX = neighborX - 1;
            }

            if (neighborX >= 0 && neighborX < width && neighborY >= 0 && neighborY < height) {
                int neighborIdx = neighborY * width + neighborX;

                if (closedSet[neighborIdx] == 0 && grid[neighborIdx] == 0) {
                    int tentativeG = gScore[current] + 1;

                    if (tentativeG < gScore[neighborIdx]) {
                        gScore[neighborIdx] = tentativeG;
                        fScore[neighborIdx] = tentativeG + manhattan(neighborX, neighborY, goalX, goalY);

                        if (openSet[neighborIdx] == 0) {
                            openSet[neighborIdx] = 1;
                        }
                    }
                }
            }

            dir = dir + 1;
        }

        iterations = iterations + 1;
    }

    return -1;
}

int width = 4;
int height = 4;
int grid = [
    0, 0, 0, 0,
    0, 1, 1, 0,
    0, 0, 0, 0,
    0, 0, 0, 0
];

int result = astar(grid, width, height, 0, 0, 3, 3);
print(result);
"""
        output = self.compile_and_execute(source)
        self.assertEqual(output, "6", "Shortest path from (0,0) to (3,3) should be 6")

    def test_astar_no_path(self):
        """Test A* when no path exists (surrounded by obstacles)."""
        source = """
function abs(int x) {
    if (x < 0) {
        return 0 - x;
    }
    return x;
}

function manhattan(int x1, int y1, int x2, int y2) {
    int dx = abs(x2 - x1);
    int dy = abs(y2 - y1);
    return dx + dy;
}

function astar(int grid, int width, int height, int startX, int startY, int goalX, int goalY) {
    int openSet = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    int closedSet = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    int gScore = [999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999];
    int fScore = [999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999];

    int startIdx = startY * width + startX;
    int goalIdx = goalY * width + goalX;

    openSet[startIdx] = 1;
    gScore[startIdx] = 0;
    fScore[startIdx] = manhattan(startX, startY, goalX, goalY);

    int iterations = 0;
    int maxIterations = 100;

    while (iterations < maxIterations) {
        int current = -1;
        int minF = 999999;

        int i = 0;
        while (i < width * height) {
            if (openSet[i] == 1 && fScore[i] < minF) {
                minF = fScore[i];
                current = i;
            }
            i = i + 1;
        }

        if (current == -1) {
            return -1;
        }

        if (current == goalIdx) {
            return gScore[current];
        }

        openSet[current] = 0;
        closedSet[current] = 1;

        int currentX = current % width;
        int currentY = current / width;

        int dir = 0;
        while (dir < 4) {
            int neighborX = currentX;
            int neighborY = currentY;

            if (dir == 0) {
                neighborY = neighborY - 1;
            }
            if (dir == 1) {
                neighborX = neighborX + 1;
            }
            if (dir == 2) {
                neighborY = neighborY + 1;
            }
            if (dir == 3) {
                neighborX = neighborX - 1;
            }

            if (neighborX >= 0 && neighborX < width && neighborY >= 0 && neighborY < height) {
                int neighborIdx = neighborY * width + neighborX;

                if (closedSet[neighborIdx] == 0 && grid[neighborIdx] == 0) {
                    int tentativeG = gScore[current] + 1;

                    if (tentativeG < gScore[neighborIdx]) {
                        gScore[neighborIdx] = tentativeG;
                        fScore[neighborIdx] = tentativeG + manhattan(neighborX, neighborY, goalX, goalY);

                        if (openSet[neighborIdx] == 0) {
                            openSet[neighborIdx] = 1;
                        }
                    }
                }
            }

            dir = dir + 1;
        }

        iterations = iterations + 1;
    }

    return -1;
}

int width = 4;
int height = 4;
int grid = [
    0, 0, 0, 0,
    0, 1, 1, 1,
    0, 1, 0, 1,
    0, 1, 1, 1
];

int result = astar(grid, width, height, 0, 0, 2, 2);
print(result);
"""
        output = self.compile_and_execute(source)
        self.assertEqual(output, "-1", "Should return -1 when no path exists")

    def test_astar_straight_line(self):
        """Test A* on a straight line path with no obstacles."""
        source = """
function abs(int x) {
    if (x < 0) {
        return 0 - x;
    }
    return x;
}

function manhattan(int x1, int y1, int x2, int y2) {
    int dx = abs(x2 - x1);
    int dy = abs(y2 - y1);
    return dx + dy;
}

function astar(int grid, int width, int height, int startX, int startY, int goalX, int goalY) {
    int openSet = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    int closedSet = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    int gScore = [999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999];
    int fScore = [999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999];

    int startIdx = startY * width + startX;
    int goalIdx = goalY * width + goalX;

    openSet[startIdx] = 1;
    gScore[startIdx] = 0;
    fScore[startIdx] = manhattan(startX, startY, goalX, goalY);

    int iterations = 0;
    int maxIterations = 100;

    while (iterations < maxIterations) {
        int current = -1;
        int minF = 999999;

        int i = 0;
        while (i < width * height) {
            if (openSet[i] == 1 && fScore[i] < minF) {
                minF = fScore[i];
                current = i;
            }
            i = i + 1;
        }

        if (current == -1) {
            return -1;
        }

        if (current == goalIdx) {
            return gScore[current];
        }

        openSet[current] = 0;
        closedSet[current] = 1;

        int currentX = current % width;
        int currentY = current / width;

        int dir = 0;
        while (dir < 4) {
            int neighborX = currentX;
            int neighborY = currentY;

            if (dir == 0) {
                neighborY = neighborY - 1;
            }
            if (dir == 1) {
                neighborX = neighborX + 1;
            }
            if (dir == 2) {
                neighborY = neighborY + 1;
            }
            if (dir == 3) {
                neighborX = neighborX - 1;
            }

            if (neighborX >= 0 && neighborX < width && neighborY >= 0 && neighborY < height) {
                int neighborIdx = neighborY * width + neighborX;

                if (closedSet[neighborIdx] == 0 && grid[neighborIdx] == 0) {
                    int tentativeG = gScore[current] + 1;

                    if (tentativeG < gScore[neighborIdx]) {
                        gScore[neighborIdx] = tentativeG;
                        fScore[neighborIdx] = tentativeG + manhattan(neighborX, neighborY, goalX, goalY);

                        if (openSet[neighborIdx] == 0) {
                            openSet[neighborIdx] = 1;
                        }
                    }
                }
            }

            dir = dir + 1;
        }

        iterations = iterations + 1;
    }

    return -1;
}

int width = 4;
int height = 4;
int grid = [
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0
];

int result = astar(grid, width, height, 0, 0, 3, 0);
print(result);
"""
        output = self.compile_and_execute(source)
        self.assertEqual(output, "3", "Straight line path should be 3 steps")


if __name__ == '__main__':
    unittest.main()
