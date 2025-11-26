import random

from pysat.solvers import Glucose3


def question1(M, N, i0, j0):
    solver = Glucose3()

    variables = {
        (s, i, j): 1 + s * M * N + i * N + j
        for s in range(M * N)
        for i in range(M)
        for j in range(N)
    }
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

    # at step 0, the knight must be in $(i_0, j_0)$
    for i in range(M):
        for j in range(N):
            if i == i0 and j == j0:
                solver.add_clause([variables[(0,i,j)]])
                break
            solver.add_clause([-variables[(0,i,j)]])

    for s in range(M*N):
        # at each step, the knight is in exactly one cell
        ## the knight is in at least one cell
        cells_at_s = []
        for i in range(M):
            for j in range(N):
                cells_at_s.append(variables[s, i, j])
        solver.add_clause(cells_at_s)
        ## the knight is in at most one cell
        for i1 in range(M):
            for j1 in range(N):
                for i2 in range(M):
                    for j2 in range(N):
                        if (i1,j1) < (i2,j2):
                            solver.add_clause(
                                [-variables[(s,i1,j1)],-variables[(s,i2,j2)]]
                            )
        # for each consecutive two steps `s` and `s+1`,
        # if the knight is in cell $(i, j)$ on step `s`,
        # then the knight must be in a cell that is accessible via a legal knight move on step `s+1`.
    for s in range(M*N - 1):
        for i in range(M):
            for j in range(N):
                possible_next_cells = []
                for di, dj in knight_moves:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < M and 0 <= nj < N:
                        possible_next_cells.append(variables[(s + 1, ni, nj)])

                solver.add_clause([-variables[(s, i, j)]] + possible_next_cells)

    # Constraint: Each cell (i, j) must be visited exactly once
    for i in range(M):
        for j in range(N):
            # 1. The cell must be visited at least once
            solver.add_clause([variables[(s, i, j)] for s in range(M * N)])

            # 2. The cell cannot be visited more than once (pairwise exclusion)
            for s1 in range(M * N):
                for s2 in range(s1 + 1, M * N):
                    solver.add_clause([-variables[(s1, i, j)], -variables[(s2, i, j)]])


# Solve
    status = solver.solve()

    # Prepare the solution grid (initialized to -1 as requested for failure cases)
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

    # YOUR CODE HERE

    return nb_sol


def question4():
    nb_sol = 0

    # YOUR CODE HERE

    return nb_sol


def question5(M, N, i0, j0):
    constraints = []

    # YOUR CODE HERE

    return constraints
