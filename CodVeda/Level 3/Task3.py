# -- N-QUEENS PROBLEM --
# Place N queens on an N×N chessboard so no two queens
# threaten each other (same row, column, or diagonal).


def create_board(n):
    # A 2D list of zeros represents an empty board.
    # board[row][col] = 1 means a queen is placed there.
    # board[row][col] = 0 means the cell is empty.
    # [[0]*n for _ in range(n)] builds n rows, each with n zeros.
    return [[0] * n for _ in range(n)]


def is_safe(board, row, col, n):
    """
    Check whether placing a queen at (row, col) is safe.
    We only need to look LEFT and UP because we place queens
    left-to-right, column by column — the right side is still empty.

    Three threats to check:
      1. Same row (left of current column)
      2. Upper-left diagonal
      3. Lower-left diagonal
    """

    # 1. Check the same row to the left
    for c in range(col):
        if board[row][c] == 1:
            return False

    # 2. Check upper-left diagonal
    # Move up-left one step at a time: row-1, col-1 then row-2, col-2 etc.
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0:
        if board[r][c] == 1:
            return False
        r -= 1
        c -= 1

    # 3. Check lower-left diagonal
    # Move down-left one step at a time
    r, c = row + 1, col - 1
    while r < n and c >= 0:
        if board[r][c] == 1:
            return False
        r += 1
        c -= 1

    return True   # no threats found — this cell is safe


def solve(board, col, n, solutions):
    """
    The core backtracking function.
    We place queens column by column (left to right).
    For each column, we try every row from top to bottom.

    Base case:  col == n means we've successfully placed a queen
                in every column → we found a complete solution.
    Recursive:  try each row in the current column. If safe, place
                the queen and recurse into the next column.
                If the recursion fails, remove the queen (backtrack)
                and try the next row.
    """

    # Base case — all N columns have a queen: solution found
    if col == n:
        # Make a deep copy of the board so storing it in solutions
        # captures the current state, not a reference that will change later.
        solutions.append([row[:] for row in board])
        return

    for row in range(n):
        if is_safe(board, row, col, n):

            # Place the queen
            board[row][col] = 1

            # Recurse: try to place a queen in the next column
            solve(board, col + 1, n, solutions)

            # Backtrack: remove the queen whether the recursion
            # succeeded or failed, so we can try the next row.
            # If it succeeded we already saved the solution above.
            # If it failed we MUST undo or the board stays dirty.
            board[row][col] = 0


def print_board(board, n, number):
    """Print one solution as a readable chessboard."""
    print(f"\nSolution {number}:")
    print("  " + " ".join(str(c + 1) for c in range(n)))   # column numbers

    for r in range(n):
        # 'Q' for queen, '.' for empty cell
        row_str = " ".join("Q" if board[r][c] == 1 else "." for c in range(n))
        print(f"{r + 1} {row_str}")   # row number then the row


def nqueens(n):
    """Entry point — sets up the board, runs the solver, prints all solutions."""
    if n < 1:
        print("N must be at least 1.")
        return

    board     = create_board(n)
    solutions = []           # will collect all complete solutions

    # Start from column 0 (the leftmost column)
    solve(board, 0, n, solutions)

    if not solutions:
        print(f"No solution exists for {n}-Queens.")
    else:
        print(f"\n{n}-Queens: {len(solutions)} solution(s) found.")
        for i, sol in enumerate(solutions, 1):
            print_board(sol, n, i)


# ── RUN ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        n = int(input("Enter N (board size): "))
        nqueens(n)
    except ValueError:
        print("Please enter a valid integer.")