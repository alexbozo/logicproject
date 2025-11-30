import random

from pysat.solvers import Glucose3

knight_moves = [
    (+2, +1),
    (+1, +2),
    (-1, +2),
    (-2, +1),
    (-2, -1),
    (-1, -2),
    (+1, -2),
    (+2, -1),
]

def question1(M, N, i0, j0):
    solver = Glucose3()

    # dict such as (s, i, j): unique ID
    variables = {
        (s, i, j): 1 + (i * N) + j + (s * M * N)
        for s in range(M * N)
        for i in range(M)
        for j in range(N)
    }

    # at step 0, the knight must be in $(i_0, j_0)$
    for i in range(M):
        for j in range(N):
            if i == i0 and j == j0:
                solver.add_clause([variables[(0, i, j)]])
                break
            solver.add_clause([-variables[(0, i, j)]])

    for s in range(M*N):
        # at each step, the knight is in exactly one cell

        ## the knight is in minimum one cell
        cells = []
        for i in range(M):
            for j in range(N):
                cells.append(variables[s, i, j])
        solver.add_clause(cells)

        ## the knight is in maximum one cell
        for i1 in range(M):
            for j1 in range(N):
                for i2 in range(M):
                    for j2 in range(N):
                        if (i1, j1) < (i2, j2): # equivalent to (i1, j1) != (i2, j2) in this case
                            solver.add_clause(
                                [-variables[(s, i1, j1)],-variables[(s, i2, j2)]]
                            )

        # for each consecutive two steps `s` and `s+1`,
        # if the knight is in cell $(i, j)$ on step `s`,
        # then the knight must be in a cell that is accessible via a legal knight move on step `s+1`.
        if s < M*N - 1:
            for i in range(M):
                for j in range(N):
                    possible_next_cells = []
                    for x, y in knight_moves:
                        next_i, next_j = i + x, j + y
                        if 0 <= next_i < M and 0 <= next_j < N:
                            possible_next_cells.append(variables[(s + 1, next_i, next_j)])
                    solver.add_clause([-variables[(s, i, j)]] + possible_next_cells)

        # for each consecutive two steps `s-1` and `s`,
        # if the knight is in cell $(i, j)$ on step `s`,
        # then the knight must have been in a valid cell on step `s-1`.
        if s >= 1:
            for i in range(M):
                for j in range(N):
                    possible_previous_cells = []
                    for di, dj in knight_moves:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < M and 0 <= nj < N:
                            possible_previous_cells.append(variables[(s - 1, ni, nj)])
                    solver.add_clause([-variables[(s, i, j)]] + possible_previous_cells)

    # Each cell (i, j) must be visited exactly once
    cells = []
    for i in range(M):
        for j in range(N):
            for s in range(M * N):
                cells.append(variables[s, i, j])
    solver.add_clause(cells)

    for i in range(M):
        for j in range(N):
            ## The cell must be visited at least once
            solver.add_clause([variables[(s, i, j)] for s in range(M * N)])

            ## The cell cannot be visited more than once (pairwise exclusion)
            for s1 in range(M * N):
                for s2 in range(s1 + 1, M * N):
                    solver.add_clause([-variables[(s1, i, j)], -variables[(s2, i, j)]])


    # Solve
    status = solver.solve()
    solution = [[-1 for _ in range(N)] for _ in range(M)]

    if status:
        model = solver.get_model()
        # Create a lookup set for faster checking
        model_set = set(model)

        # Fill the solution grid
        for s in range(M * N):
            for i in range(M):
                for j in range(N):
                    # If the variable for (s, i, j) is in the model (True)
                    if variables[(s, i, j)] in model_set:
                        solution[i][j] = s

    return solution, solver, variables


def question3():
    nb_sol = 0

    for i0 in range(3):
        for j0 in range(4):
            solution, solver, _ = question1(3, 4, i0, j0)
            if solution[0][0] == -1: # invalid solution
                continue
            while solver.solve():
                nb_sol += 1
                model = solver.get_model()
                path = []
                for n in model:
                    if n > 0:
                        path.append(-n)
                solver.add_clause(path)

    return nb_sol


def question4():
    nb_sol = 0
    found_solutions = set()

    sym_cells = {}
    for i in range(3):
        for j in range(4):
            sym_cells[(i, j)] = {
                (2 - i, j),
                (i, 3 - j),
                (2 - i, 3 - j)
            }

    for i in range(3):
        for j in range(4):
            solution_template, solver, variables = question1(3, 4, i, j)

            if solution_template[0][0] == -1:
                continue

            while solver.solve():
                model = solver.get_model()
                current_grid = [[0] * 3 for _ in range(4)] # 2D grid (M*N) initialized to 0
                model_set = set(model)

                # get current grid
                for s in range(3 * 4):
                    for i in range(3):
                        for j in range(4):
                            if variables[(s, i, j)] in model_set:
                                current_grid[i][j] = s

                # convert current grid to tuples for unicity
                grid_tuple = tuple(tuple(row) for row in current_grid)


                is_new = True
                for sym_grid in get_symmetries(grid_tuple):
                    if sym_grid in found_solutions:
                        is_new = False
                        break

                if is_new:
                    found_solutions.add(grid_tuple)

                path = [-x for x in model if x > 0]
                solver.add_clause(path)
    nb_sol = len(found_solutions)
    return nb_sol


def question5(M, N, i0, j0):
    def is_solution_unique(solver):

        return False

    constraints = []

    solution, solver, variables = question1(M, N, i0, j0)
    if solution[0][0] == -1:
        return constraints

    if is_solution_unique(solver):
        return [(0, i0, j0)]



    return constraints
