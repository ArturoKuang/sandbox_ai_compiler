# SimpleLang Algorithm Implementations

This document describes the three classic algorithms implemented in SimpleLang (.sl) to demonstrate the language's capabilities.

## Overview

The following algorithms have been implemented in SimpleLang:

1. **Dijkstra's Algorithm** - Shortest path in weighted graphs
2. **A* Pathfinding** - Heuristic-based pathfinding in grids
3. **N-Queens** - Recursive backtracking solution

All implementations demonstrate SimpleLang's support for:
- Functions with parameters and return values
- Recursive function calls
- Arrays and array access
- While loops
- Conditional statements (if/else)
- Integer arithmetic

## Algorithm Details

### 1. Dijkstra's Algorithm

**File**: `examples/dijkstra.sl`

**Purpose**: Finds the shortest path between two nodes in a weighted graph.

**Implementation Details**:
- Uses adjacency matrix representation (flattened 2D array)
- Maintains distance array and visited array
- Iteratively selects unvisited node with minimum distance
- Updates distances to neighbors

**Example**:
```bash
python simplelang.py examples/dijkstra.sl --run
```

**Expected Output**: `11` (shortest path from node 0 to node 5 in the example graph)

**Test Cases**:
- Simple 4-node graph
- Graph with no path
- Same source and destination
- Complex 6-node graph

### 2. A* Pathfinding

**File**: `examples/astar.sl`

**Purpose**: Finds the shortest path in a grid with obstacles using the A* algorithm.

**Implementation Details**:
- Uses Manhattan distance as heuristic
- Maintains open set (frontier) and closed set (visited)
- Tracks g-score (cost from start) and f-score (g-score + heuristic)
- Explores 4-directional movement (up, down, left, right)

**Helper Functions**:
- `abs(x)`: Absolute value
- `manhattan(x1, y1, x2, y2)`: Manhattan distance heuristic

**Example**:
```bash
python simplelang.py examples/astar.sl --run
```

**Expected Output**: `6` (path length from (0,0) to (3,3) in a 4x4 grid with obstacles)

**Test Cases**:
- Simple path with obstacles
- No path (goal surrounded by obstacles)
- Straight line path with no obstacles

### 3. N-Queens (Recursive)

**File**: `examples/nqueens.sl`

**Purpose**: Solves the N-Queens problem using recursive backtracking.

**Implementation Details**:
- Places queens column by column
- Checks row, upper diagonal, and lower diagonal for safety
- Uses recursion to try all valid positions
- Backtracks when no valid position is found

**Helper Functions**:
- `abs(x)`: Absolute value (not used but available)
- `isSafe(board, n, row, col)`: Checks if placing a queen is safe
- `solveNQueensUtil(board, n, col)`: Recursive solver
- `solveNQueens(n)`: Main entry point

**Example**:
```bash
python simplelang.py examples/nqueens.sl --run
```

**Expected Output**: `1` (solution found for 4x4 board)

**Test Cases**:
- 1x1 board (trivial solution)
- 2x2 board (no solution)
- 3x3 board (no solution)
- 4x4 board (solution exists)

## Running the Tests

### Individual Test Suites

Run tests for a specific algorithm:

```bash
# Dijkstra tests
python -m unittest tests/algorithms/test_dijkstra.py -v

# A* tests
python -m unittest tests/algorithms/test_astar.py -v

# N-Queens tests
python -m unittest tests/algorithms/test_nqueens.py -v
```

### All Algorithm Tests

Run all algorithm tests at once:

```bash
python run_algorithm_tests.py
```

Or using unittest directly:

```bash
python -m unittest tests/algorithms/test_dijkstra.py \
                   tests/algorithms/test_astar.py \
                   tests/algorithms/test_nqueens.py -v
```

## Test Coverage

### Dijkstra (4 tests)
- ✓ Simple graph shortest path
- ✓ No path exists
- ✓ Same source and destination
- ✓ Complex 6-node graph

### A* (3 tests)
- ✓ Simple path with obstacles
- ✓ No path exists (blocked)
- ✓ Straight line path

### N-Queens (4 tests)
- ✓ 1x1 board (trivial case)
- ✓ 2x2 board (no solution)
- ✓ 3x3 board (no solution)
- ✓ 4x4 board (has solution)

**Total**: 11 test cases covering edge cases and normal operation.

## Language Features Demonstrated

The algorithm implementations showcase SimpleLang's capabilities:

1. **Functions**:
   - Declaration with typed parameters
   - Return values
   - Function calls within functions
   - Recursive function calls

2. **Data Types**:
   - Integers
   - Arrays (fixed-size)
   - Array indexing with computed indices

3. **Control Flow**:
   - While loops
   - If/else conditionals
   - Nested control structures

4. **Expressions**:
   - Arithmetic operations (+, -, *, /, %)
   - Comparison operations (<, >, <=, >=, ==, !=)
   - Logical operations (&&, ||)
   - Array access and assignment

5. **Advanced Features**:
   - Recursion (N-Queens)
   - Multi-dimensional array simulation (flattened arrays)
   - Helper function composition (A* uses abs and manhattan)

## Compiler Fix

During testing, a scoping issue was identified and fixed in the compiler:

**Issue**: When using `python simplelang.py file.sl --run`, function definitions
were not accessible in the execution scope due to improper use of `exec()`.

**Fix**: Modified `simplelang.py` to provide a proper namespace to `exec()`:

```python
# Before
exec(python_code)

# After
namespace = {}
exec(python_code, namespace)
```

This ensures all function definitions are properly scoped and accessible during execution.

## Future Enhancements

Potential improvements to the algorithms or language:

1. **Language Features**:
   - Dynamic arrays or lists
   - For loops (currently supported but not used in these examples)
   - String support
   - Better array initialization syntax

2. **Algorithm Enhancements**:
   - Return the actual path (not just distance/existence)
   - Count all solutions (N-Queens)
   - Bidirectional Dijkstra
   - Different heuristics for A*

3. **Test Improvements**:
   - Performance benchmarks
   - Larger problem instances
   - Comparison with Python implementations
