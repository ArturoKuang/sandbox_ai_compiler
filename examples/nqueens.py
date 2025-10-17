def abs(x: int) -> int:
    if (x < 0):
        return (0 - x)
    return x

def isSafe(board: int, n: int, row: int, col: int) -> int:
    i: int = 0
    while (i < col):
        if (board[((row * n) + i)] == 1):
            return 0
        i = (i + 1)
    r: int = row
    c: int = col
    while ((r >= 0) and (c >= 0)):
        if (board[((r * n) + c)] == 1):
            return 0
        r = (r - 1)
        c = (c - 1)
    r = row
    c = col
    while ((r < n) and (c >= 0)):
        if (board[((r * n) + c)] == 1):
            return 0
        r = (r + 1)
        c = (c - 1)
    return 1

def solveNQueensUtil(board: int, n: int, col: int) -> int:
    if (col >= n):
        return 1
    row: int = 0
    while (row < n):
        if (isSafe(board, n, row, col) == 1):
            board[((row * n) + col)] = 1
            result: int = solveNQueensUtil(board, n, (col + 1))
            if (result == 1):
                return 1
            board[((row * n) + col)] = 0
        row = (row + 1)
    return 0

def solveNQueens(n: int) -> int:
    board: int = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    result: int = solveNQueensUtil(board, n, 0)
    return result

n: int = 4
result: int = solveNQueens(n)
print(result)