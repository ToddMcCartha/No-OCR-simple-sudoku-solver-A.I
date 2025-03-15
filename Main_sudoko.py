from sudoku_detector import SudokuDetector
from sudoku_solver import SudokuSolver
from sudoku_printer import SudokuPrinter
import cv2

#Uncomment the line underneath if using Linux
#TEMPLATE_DIR = "templates"

#Uncomment the line underneath if using Windows
#TEMPLATE_DIR = directory_path = r"C:\"templates""

#Also make sure you have the templates folder in the right location
#with all the .png images of 0-9 "0 is a white blank image"
#or this script work or run properly.
def main():
    #change the location of your webcam
    #down below, no need change if you are using
    #your laptop's builtin camera.
    cap = cv2.VideoCapture(0)
    detector = SudokuDetector(TEMPLATE_DIR)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame.")
            break

        result = detector.detect_board(frame)
        if result:
            board, warped = result
            print("Detected Sudoku Board:")
            SudokuPrinter.print_board(board)

            solver = SudokuSolver(board)
            if solver.solve():
                print("Solved Sudoku Board:")
                SudokuPrinter.print_board(board)

                # -----------------------------------------------
                # Rotate the warped image once more for final display
                # Change ROTATE_90_COUNTERCLOCKWISE to ROTATE_90_CLOCKWISE
                # if you want the other sideways orientation.
                warped = cv2.rotate(warped, cv2.ROTATE_90_CLOCKWISE)
                # -----------------------------------------------

                # Display the rotated warped image with the solution overlaid
                SudokuPrinter.print_on_warped_image(warped, board)
            else:
                print("No solution found.")

        cv2.imshow("Live Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
