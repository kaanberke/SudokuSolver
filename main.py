import ac3
import backtracking
import time
import matplotlib.pyplot as plt
import sys


def main(input_file, output_file):
    backtracking_time, ac3_time = [0], [0]

    lines = input_file.readlines()[:500]
    total = len(lines)
    print(f"{total} number of sudoku puzzles are being solved.")
    print("-" * 55)
    result = {
        "solved": 0,
        "no solution": 0
    }

    start = time.time()
    for line in lines:
        current = time.time()
        answer = ac3.main(line)
        ac3_time.append(ac3_time[-1] + time.time() - current)
        if answer:
            result["solved"] += 1
        else:
            result["no solution"] += 1

    print(f"{result['solved']} solved by using AC3")
    print(f"{result['no solution']} could not solved")
    print(f"It took {time.time() - start} second(s) to solved {result['solved']} number of sudoku puzzles.")
    print("-" * 55)

    result["solved"], result["no solution"] = 0, 0
    start = time.time()
    for line in lines:
        current = time.time()
        answer = backtracking.main(line)
        backtracking_time.append(backtracking_time[-1] + time.time() - current)
        if answer:
            result["solved"] += 1
            output_file.write(answer)
        else:
            result["no solution"] += 1

    print(f"{result['solved']} solved by using Backtracking")
    print(f"{result['no solution']} could not solved")
    print(f"It took {time.time() - start} second(s) to solved {result['solved']} number of sudoku puzzles.")

    backtracking_time.pop(0)
    ac3_time.pop(0)
    return backtracking_time, ac3_time


if __name__ == "__main__":
    try:
        input_file = open(sys.argv[1], "r")
        output_file = open(sys.argv[2], "w")
        # input_file = open("input copy.txt", "r")
        # output_file = open("output.txt", "w")

        backtracking_time, ac3_time = main(input_file, output_file)
        plt.plot([i + 1 for i in range(500)], ac3_time, c="red", label="AC3")
        plt.plot([i + 1 for i in range(500)], backtracking_time, c="blue", label="Backtracking")
        plt.legend()
        plt.xlabel('Number of sudoku puzzles')
        plt.ylabel('Solving time in seconds')
        plt.show()
    except:
        # Just in case for now..
        raise Exception("Something went wrong!")
    finally:
        input_file.close()
        output_file.close()
