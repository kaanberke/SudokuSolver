import copy
import csv
import time
import os


class Sudoku(object):
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.ans = copy.deepcopy(puzzle)
        self.num_of_assignments = 0
        self.num_of_empty = 0

    def show_board(self):
        to_be_printed = self.puzzle
        if type(self.puzzle) == list:
            temp = ""
            for row in self.puzzle:
                for col in row:
                    temp += str(col)
            to_be_printed = temp
        for i in range(len(to_be_printed)):
            print(to_be_printed[i], end=" ", sep="")
            if (i+1) % 3 == 0 and i != 0 and i % 9 != 8:
                print("| ", end="", sep="")
            if (i+1) % 9 == 0:
                print("")
                if (i+1) % 27 == 0 and (i+1) % 81 != 0:
                    print("-"*21)

    def solve(self):
        initial_domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # Their IDs are different. Basically, they are different lists..!
        transformed_puzzle = copy.deepcopy(self.puzzle)
        # Count the number of empty slots..!
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] == 0:
                    self.num_of_empty += 1

        # If a slot is 0 then replace it with domain for our deep copied list..!
        # Such as, [2, 4, 0, 6, 7] => [2, 4, [1, 2, 3, 4, 5, 6, 7, 8, 9], 6, 7]..!
        for row_index, row in enumerate(self.puzzle):
            for col_index, value in enumerate(row):
                if value == 0:
                    transformed_puzzle[row_index][col_index] = initial_domain[::]
                else:
                    transformed_puzzle[row_index][col_index] = value

        # in AC3,
        # loop through queue constraints tuple
        result_ac3 = ""
        self.AC3(transformed_puzzle)
        for row in transformed_puzzle:
            for col in row:
                result_ac3 += str(col) if type(col) == int else str(col[0])
        self.puzzle = result_ac3
        return result_ac3

    def getNumOfUnassignedNeighbours(self, csp, var):
        neighbours = self.get_neighbouring_constraints(var)
        total = 0
        for neighbour in neighbours:
            if not self.isAssigned(csp[neighbour[0]][neighbour[1]]):
                total += 1
        return total

    def isAssigned(self, i):
        return type(i) == int


    # index is a tuple with (row, col)
    def get_neighbouring_constraints(self, index):

        neighbours = set()

        # Get neighbors from same column..!
        for row_index in range(0, 9):
            # (row_index, col_index)
            neighbours.add((row_index, index[1]))

        # Get neighbors from same row..!
        for col_index in range(0, 9):
            neighbours.add((index[0], col_index))

        """ 
            My favorite part, get the box neighbors..!
            First of all, get the top left index of the parterre that we need to find neighbors of..!
            Let's say our indexes are = (4, 4) which is exactly middle of the board..!
            Then we need to find indexes of (3, 3)..!
            As we all know, there are 9 parterre on a sudoku board and they all 3x3..!
            If we divide our indexes by 3 and get the remainder for both than we get the indexes for just the parterre
           which we already in it..!
            I mean, if we 4 % 3 then it returns 1 as a remainder. For a parterre which is 3x3, our value is on the index
           of 1x1 and that is all we were looking for..!
            Now we easily get all parterre and check it because now we know that top left is 0x0 and we are in 1x1 which
           means we are going to subtract 1 from each original index..!
        """
        #              (   4     - (      1     ),     4    - (      1     )) = (3, 3)
        topLeftOfBox = (index[0] - (index[0] % 3), index[1] - (index[1] % 3))

        for i in range(topLeftOfBox[0], topLeftOfBox[0] + 3):
            for j in range(topLeftOfBox[1], topLeftOfBox[1] + 3):
                neighbours.add((i, j))

        # We should remove our target index because it is not int..!
        neighbours.remove(index)

        # Return whole the neighbours which includes col, row and parterre as a list format..!
        return list(neighbours)

    # Modifies CSP directly
    # Returns False if not consistent
    def AC3(self, csp):
        # define initial constraints into a queue
        queue_constraint_tuple = []
        for row_index, row in enumerate(csp):
            for col_index, value in enumerate(row):
                if not self.isAssigned(value):  # Checks whether value is int or not..!
                    # Get all available neighbours..!
                    neighbours = self.get_neighbouring_constraints((row_index, col_index))

                    # Create a constraint tuple to restrict our area..!
                    constraints = [((row_index, col_index), neighbour) for neighbour in neighbours]

                    # Put all restricted area tuples into together..!
                    queue_constraint_tuple += constraints

        # Let's start to process our restricted tuples one by one until there is no more..!
        while queue_constraint_tuple:
            # We start to work on them from end to beginning..!
            constraint = queue_constraint_tuple.pop()
            # csp is our target place (value), constraint tuple is one of the neighbors..!
            if self.revise(csp, constraint[0], constraint[1]):

                # If the length of the neighbor is zero then return False..!
                if len(csp[constraint[0][0]][constraint[0][1]]) == 0:
                    return False

                # Here we go again... Now this time, we get the neighbors which is left..!
                neighbouring_arcs = self.get_neighbouring_constraints(constraint[0])

                # Now we remove the former neighbor that we just inspected..!
                neighbouring_arcs.remove(constraint[1])

                # Now this time wee add our neighbours to queue as a target value and
                # we add our former target to queue as a constraint(neighbor) of it..!
                for arc in neighbouring_arcs:
                    if not self.isAssigned(csp[arc[0]][arc[1]]):
                        queue_constraint_tuple.append((arc, constraint[0]))
        return True

    # CSP is list of list of domain or assigned value
    # CSP shouldn't be a deepcopy!
    # Domain would be a list of integer, assignment value would be an integer
    def revise(self, csp, i, j):
        iDomain = csp[i[0]][i[1]]  # Must be a list, cannot be assigned
        jDomain = csp[j[0]][j[1]]  # Might be already assigned, or a list

        # If the neighbor is already assigned..!
        if type(jDomain) == int:
            # If our target place(value) involves the assigned neighbor then remove it..!
            if jDomain in iDomain:
                iDomain.remove(jDomain)
                return True
            return False

        # But if the neighbor isn't assigned then we check the list of it whether
        # it is length is sufficient or not..!
        if len(jDomain) <= 1:
            # If it's length is 1 or 0 then it will be handled later and check its last item for this case..!
            if jDomain[0] in iDomain:
                iDomain.remove(jDomain[0])
                return True
        return False


def main(board=None, line=None):
    if board is None:
        # return None
        board = "004300209005009001070060043006002087190007400050083000600000105003508690042910300"
    puzzle = [[0 for i in range(9)] for j in range(9)]
    i, j = 0, 0
    for number in board:
        if '0' <= number <= '9':
            puzzle[i][j] = int(number)
            j += 1
            if j == 9:
                i += 1
                j = 0

    sudoku = Sudoku(puzzle)
    #sudoku.show_board()
    ans = sudoku.solve()
    if ans:
        #print(f"Solution for Sudoku number: {line}")
        #sudoku.show_board()
        return ans
        # If we decide to return it as a list..!
        # return "".join(map(str, list(ans[i][j] for j in range(9) for i in range(9))))
    else:
        print(f"There is not solution for Sudoku number: {line}")
        return False


if __name__ == "__main__":
    with open('sudoku.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        solved = 0
        start = time.time()
        for line, row in enumerate(csv_reader, 1):
            if line == 1:
                continue
            if main(row[0], line-1):
                solved += 1
            else:
                print("THERE IS NO SOLUTION!")
            input("Please press any key to continue..")
            print("\n"*4)
            os.system('clear')
        print(f"1 million sudoku puzzles solved in {time.time() - start} seconds.")