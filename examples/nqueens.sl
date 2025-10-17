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
