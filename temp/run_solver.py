from matching_problems import solver

args = ['-na', '3', '-maxsize', '1', '-gen', '2', '-lsb', '3']

data = {
    "students": [
        [1, 7],
        [1, 2, 3, 4, 5, 6],
        [2, 1, 4],
        [2],
        [1, 2, 3, 4],
        [2, 3, 4, 5, 6],
        [5, 3, 8]
    ],
    "projects": [
        [0, 2, 1],
        [0, 1, 1],
        [0, 1, 1],
        [0, 1, 2],
        [0, 1, 2],
        [0, 1, 2],
        [0, 1, 3],
        [0, 1, 3],
    ],
    "lecturers": [
        [0, 2, 3],
        [0, 2, 2],
        [0, 2, 2]
    ],
}


if __name__ == "__main__":
    solver = solver.Solver(args, data)
    solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    # print(solver.get_debug())
    # print(solver.get_results_long())
    # print(solver.get_results_short())
    print(solver.get_results())
