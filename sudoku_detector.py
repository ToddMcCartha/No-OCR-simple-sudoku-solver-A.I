import cv2
import numpy as np
import os

def order_points(pts):
    # Initialize a list of coordinates that will be ordered
    # such that the first entry is the top-left,
    # the second is the top-right, the third is the bottom-right,
    # and the fourth is the bottom-left.
    rect = np.zeros((4, 2), dtype="float32")
    # Sum will be smallest for top-left, largest for bottom-right
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # Difference will be smallest for top-right, largest for bottom-left
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

class SudokuDetector:
    def __init__(self, template_dir):
        self.template_dir = template_dir
        self.number_to_int = {str(i): i for i in range(10)}

    def detect_digit(self, cell_image):
        max_score = 0
        detected_digit = None

        for filename in os.listdir(self.template_dir):
            if filename.endswith(".png"):
                number_name = filename.split('.')[0]
                if number_name in self.number_to_int:
                    label = self.number_to_int[number_name]
                    template_path = os.path.join(self.template_dir, filename)
                    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
                    _, template_thresh = cv2.threshold(
                        template, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
                    )

                    for scale in np.linspace(0.8, 1.2, 5):  # Scale templates
                        scaled_template = cv2.resize(
                            template_thresh,
                            None,
                            fx=scale,
                            fy=scale,
                            interpolation=cv2.INTER_LINEAR,
                        )
                        result = cv2.matchTemplate(
                            cell_image, scaled_template, cv2.TM_CCOEFF_NORMED
                        )
                        _, score, _, _ = cv2.minMaxLoc(result)
                        if score > max_score:
                            max_score = score
                            detected_digit = label

        return detected_digit, max_score

    def is_blank_cell(self, cell_image):
        avg_pixel_value = np.mean(cell_image)
        return avg_pixel_value > 170  # Threshold for blank cells

    def detect_board(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 30, 100)

        contours, _ = cv2.findContours(
            edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        max_area = 0
        puzzle_board_contour = None

        for cnt in contours:
            area = cv2.contourArea(cnt)
            epsilon = 0.02 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            if len(approx) == 4 and 66000 < area < 95000:
                if area > max_area:
                    max_area = area
                    puzzle_board_contour = approx
                    cv2.drawContours(frame, [puzzle_board_contour], -1, (0, 255, 0), 2)

        if puzzle_board_contour is not None:
            # Order the corners consistently
            pts = puzzle_board_contour.reshape(4, 2)
            ordered_pts = order_points(pts)
            pts2 = np.float32([[0, 0], [600, 0], [600, 600], [0, 600]])
            M = cv2.getPerspectiveTransform(ordered_pts, pts2)
            warped = cv2.warpPerspective(gray, M, (600, 600))

            # Use the warped image directly for digit extraction (no extra rotation/flip)
            _, binary = cv2.threshold(warped, 127, 255, cv2.THRESH_BINARY)

            cell_size = 600 // 9
            sudoku_board = [[0 for _ in range(9)] for _ in range(9)]

            for i in range(9):
                for j in range(9):
                    x, y = j * cell_size, i * cell_size
                    cell = binary[y : y + cell_size, x : x + cell_size]
                    _, cell_thresh = cv2.threshold(
                        cell, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
                    )

                    if self.is_blank_cell(cell_thresh):
                        sudoku_board[i][j] = 0
                    else:
                        detected_digit, score = self.detect_digit(cell_thresh)
                        if detected_digit is not None and score > 0.5:
                            sudoku_board[i][j] = detected_digit

            # Return the detected board and the consistently oriented warped image
            rotate = cv2.rotate(warped, cv2.ROTATE_90_COUNTERCLOCKWISE)
            flipped = cv2.flip(rotate,2)
            return sudoku_board, rotate


        return None
