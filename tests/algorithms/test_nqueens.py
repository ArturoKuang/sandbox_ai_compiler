"""
Unit tests for N-Queens recursive algorithm implementation in SimpleLang.
"""

import unittest
import subprocess
import os


class TestNQueensAlgorithm(unittest.TestCase):
    """Test cases for N-Queens recursive solution."""

    def compile_and_execute(self, source: str) -> str:
        """Helper method to compile and execute SimpleLang code."""
        # Write source to temporary file
        temp_file = "temp_test.sl"
        with open(temp_file, 'w') as f:
            f.write(source)

        try:
            # Compile the file first
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

    def test_nqueens_4x4(self):
        """Test N-Queens for 4x4 board (should find a solution)."""
        source = """
function abs(int x) {
    if (x < 0) {
        return 0 - x;
    }
    return x;
}

function isSafe(int board, int n, int row, int col) {
    int i = 0;
    while (i < col) {
        if (board[row * n + i] == 1) {
            return 0;
        }
        i = i + 1;
    }

    int r = row;
    int c = col;
    while (r >= 0 && c >= 0) {
        if (board[r * n + c] == 1) {
            return 0;
        }
        r = r - 1;
        c = c - 1;
    }

    r = row;
    c = col;
    while (r < n && c >= 0) {
        if (board[r * n + c] == 1) {
            return 0;
        }
        r = r + 1;
        c = c - 1;
    }

    return 1;
}

function solveNQueensUtil(int board, int n, int col) {
    if (col >= n) {
        return 1;
    }

    int row = 0;
    while (row < n) {
        if (isSafe(board, n, row, col) == 1) {
            board[row * n + col] = 1;

            int result = solveNQueensUtil(board, n, col + 1);
            if (result == 1) {
                return 1;
            }

            board[row * n + col] = 0;
        }
        row = row + 1;
    }

    return 0;
}

function solveNQueens(int n) {
    int board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

    int result = solveNQueensUtil(board, n, 0);
    return result;
}

int n = 4;
int result = solveNQueens(n);
print(result);
"""
        output = self.compile_and_execute(source)
        self.assertEqual(output, "1", "4-Queens should have a solution")

    def test_nqueens_1x1(self):
        """Test N-Queens for 1x1 board (trivial case)."""
        source = """
function abs(int x) {
    if (x < 0) {
        return 0 - x;
    }
    return x;
}

function isSafe(int board, int n, int row, int col) {
    int i = 0;
    while (i < col) {
        if (board[row * n + i] == 1) {
            return 0;
        }
        i = i + 1;
    }

    int r = row;
    int c = col;
    while (r >= 0 && c >= 0) {
        if (board[r * n + c] == 1) {
            return 0;
        }
        r = r - 1;
        c = c - 1;
    }

    r = row;
    c = col;
    while (r < n && c >= 0) {
        if (board[r * n + c] == 1) {
            return 0;
        }
        r = r + 1;
        c = c - 1;
    }

    return 1;
}

function solveNQueensUtil(int board, int n, int col) {
    if (col >= n) {
        return 1;
    }

    int row = 0;
    while (row < n) {
        if (isSafe(board, n, row, col) == 1) {
            board[row * n + col] = 1;

            int result = solveNQueensUtil(board, n, col + 1);
            if (result == 1) {
                return 1;
            }

            board[row * n + col] = 0;
        }
        row = row + 1;
    }

    return 0;
}

function solveNQueens(int n) {
    int board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

    int result = solveNQueensUtil(board, n, 0);
    return result;
}

int n = 1;
int result = solveNQueens(n);
print(result);
"""
        output = self.compile_and_execute(source)
        self.assertEqual(output, "1", "1-Queens should have a solution (trivial)")

    def test_nqueens_2x2(self):
        """Test N-Queens for 2x2 board (no solution exists)."""
        source = """
function abs(int x) {
    if (x < 0) {
        return 0 - x;
    }
    return x;
}

function isSafe(int board, int n, int row, int col) {
    int i = 0;
    while (i < col) {
        if (board[row * n + i] == 1) {
            return 0;
        }
        i = i + 1;
    }

    int r = row;
    int c = col;
    while (r >= 0 && c >= 0) {
        if (board[r * n + c] == 1) {
            return 0;
        }
        r = r - 1;
        c = c - 1;
    }

    r = row;
    c = col;
    while (r < n && c >= 0) {
        if (board[r * n + c] == 1) {
            return 0;
        }
        r = r + 1;
        c = c - 1;
    }

    return 1;
}

function solveNQueensUtil(int board, int n, int col) {
    if (col >= n) {
        return 1;
    }

    int row = 0;
    while (row < n) {
        if (isSafe(board, n, row, col) == 1) {
            board[row * n + col] = 1;

            int result = solveNQueensUtil(board, n, col + 1);
            if (result == 1) {
                return 1;
            }

            board[row * n + col] = 0;
        }
        row = row + 1;
    }

    return 0;
}

function solveNQueens(int n) {
    int board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

    int result = solveNQueensUtil(board, n, 0);
    return result;
}

int n = 2;
int result = solveNQueens(n);
print(result);
"""
        output = self.compile_and_execute(source)
        self.assertEqual(output, "0", "2-Queens should have no solution")

    def test_nqueens_3x3(self):
        """Test N-Queens for 3x3 board (no solution exists)."""
        source = """
function abs(int x) {
    if (x < 0) {
        return 0 - x;
    }
    return x;
}

function isSafe(int board, int n, int row, int col) {
    int i = 0;
    while (i < col) {
        if (board[row * n + i] == 1) {
            return 0;
        }
        i = i + 1;
    }

    int r = row;
    int c = col;
    while (r >= 0 && c >= 0) {
        if (board[r * n + c] == 1) {
            return 0;
        }
        r = r - 1;
        c = c - 1;
    }

    r = row;
    c = col;
    while (r < n && c >= 0) {
        if (board[r * n + c] == 1) {
            return 0;
        }
        r = r + 1;
        c = c - 1;
    }

    return 1;
}

function solveNQueensUtil(int board, int n, int col) {
    if (col >= n) {
        return 1;
    }

    int row = 0;
    while (row < n) {
        if (isSafe(board, n, row, col) == 1) {
            board[row * n + col] = 1;

            int result = solveNQueensUtil(board, n, col + 1);
            if (result == 1) {
                return 1;
            }

            board[row * n + col] = 0;
        }
        row = row + 1;
    }

    return 0;
}

function solveNQueens(int n) {
    int board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

    int result = solveNQueensUtil(board, n, 0);
    return result;
}

int n = 3;
int result = solveNQueens(n);
print(result);
"""
        output = self.compile_and_execute(source)
        self.assertEqual(output, "0", "3-Queens should have no solution")


if __name__ == '__main__':
    unittest.main()
