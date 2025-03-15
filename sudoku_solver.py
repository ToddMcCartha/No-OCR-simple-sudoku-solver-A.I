class SudokuSolver:
    def __init__(self, board):
        self.board = board

    def is_valid(self, num, pos):
        row, col = pos
        for i in range(9):
            if self.board[row][i] == num and col != i:
                return False
            if self.board[i][col] == num and row != i:
                return False
        box_x, box_y = col // 3, row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False
        return True

    def solve(self):
        empty = self.find_empty()
        if not empty:
            return True
        row, col = empty
        for num in range(1, 10):
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = 0
        return False

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None
