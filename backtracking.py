import csv
import time
import os


class Sudoku:
    def __init__(self, board=None):
        if board is None:
            self.board = ("306508400"
                          "520000000"
                          "087000031"
                          "003010080"
                          "900863005"
                          "050090600"
                          "130000250"
                          "000000074"
                          "005206300")
        else:
            self.board = board

    def show_board(self):
        for i in range(len(self.board)):
            print(self.board[i], end=" ", sep="")
            if (i + 1) % 3 == 0 and i != 0 and i % 9 != 8:
                print("| ", end="", sep="")
            if (i + 1) % 9 == 0:
                print("")
                if (i + 1) % 27 == 0 and (i + 1) % 81 != 0:
                    print("-" * 21)

    def find_empty_location(self):
        for i in range(len(self.board)):
            if (self.board[i] == "0"):
                empty_index = i
                return empty_index
        return False

    def used_in_row(self, empty_index, num):
        row = empty_index // 9
        for i in range(9):
            if self.board[row * 9 + i] == str(num):
                return True
        return False

    def used_in_col(self, empty_index, num):
        col_parter = (empty_index // 3) % 3
        col = (col_parter * 3) + (empty_index % 3)

        for i in range(9):
            if self.board[col + i * 9] == str(num):
                return True
        return False

    def used_in_box(self, empty_index, num):
        row_parter = empty_index // 27
        col_parter = (empty_index // 3) % 3

        for i in range(3):
            for j in range(3):
                if str(num) == self.board[(row_parter * 27) + (col_parter * 3) + (i * 9) + j]:
                    return True
        return False

    def check_location_is_safe(self, empty_index, num):
        # Check if 'num' is not already placed in current row,
        # current column and current 3x3 box
        return not self.used_in_row(empty_index, num) and \
               not self.used_in_col(empty_index, num) and \
               not self.used_in_box(empty_index, num)

    def solve(self):
        empty_index = 0
        # empty_index = self.find_empty_location()
        # if empty_index is False:
        #     return False
        for i in range(len(self.board)):
            if self.board[i] == "0":
                empty_index = i
                break
            elif i == len(self.board) - 1:
                return True

        for num in range(1, 10):
            if self.check_location_is_safe(empty_index, num):
                self.board = self.board[:empty_index] + str(num) + self.board[empty_index + 1:]
                if self.solve():
                    return True

                self.board = self.board[:empty_index] + "0" + self.board[empty_index + 1:]
        # this triggers backtracking
        return False


def main(board=None):
    if board is None:
        return None
    sudoku = Sudoku(board)
    if sudoku.solve():
        return sudoku.board
    else:
        return False


if __name__ == "__main__":
    with open('sudoku.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        solved = 0
        start = time.time()
        for line, row in enumerate(csv_reader, 1):
            if line == 1:
                continue
            sudoku = Sudoku(row[0])
            sudoku.show_board()
            if sudoku.solve():
                print(f"Solution for Sudoku number: {line}")
                solved += 1
                sudoku.show_board()
            else:
                print("THERE IS NO SOLUTION!")
            os.system('clear')
            # print('\n' * 80)
            # print(f"No solution for Sudoku number: {line}!")
            # input("Please press any key to continue..")
            # print("\n"*4)
        print(f"1 million sudoku puzzles solved in {time.time() - start} seconds.")
