import cv2
import time

class SudokuPrinter:
    @staticmethod
    def print_board(board):
        time.sleep(0.5)
        for row in board:
            print(" ".join(str(num) if num != 0 else "." for num in row))
        time.sleep(0.5)

    @staticmethod
    def print_on_warped_image(warped, board):
        # Convert the warped grayscale image to BGR for colored text
        display_img = cv2.cvtColor(warped.copy(), cv2.COLOR_GRAY2BGR)
        cell_size = 600 // 9

        for i in range(9):
            for j in range(9):
                text = str(board[i][j])
                # Calculate text position (approximately centered in the cell)
                x = j * cell_size + cell_size // 4
                y = i * cell_size + 3 * cell_size // 4
                cv2.putText(display_img, text, (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Warped Sudoku Solution", display_img)
        # Wait indefinitely until a key is pressed, then close the window
        cv2.waitKey(0)
        cv2.destroyWindow("Warped Sudoku Solution")
