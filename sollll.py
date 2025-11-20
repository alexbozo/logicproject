# ------------------------------------------------
# 1. Variable indexing
# Each variable x_{t,i,j} means: “At time t, knight is at cell (i,j)”
# We map (t,i,j) → SAT variable index (positive integer)
# ------------------------------------------------
variables = {
    (t, i, j): 1 + t * M * N + i * N + j
    for t in range(M * N)
    for i in range(M)
    for j in range(N)
}

# ------------------------------------------------
# 2. Constraints
# ------------------------------------------------

# (a) Exactly one position per time step
for t in range(M * N):
    # At least one
    vars_at_t = [variables[(t, i, j)] for i in range(M) for j in range(N)]
    solver.add_clause(vars_at_t)
    # at most one
    for i1 in range(M):
        for j1 in range(N):
            for i2 in range(M):
                for j2 in range(N):
                    if (i1,j1) < (i2,j2):
                        solver.add_clause(
                            [-variables[(t,i1,j1)],-variables[(t,i2,j2)]]
                        )

# (b) Each cell visited exactly once
for i in range(M):
        for j in range(N):
            vars_for_cell = [variables[(t, i, j)] for t in range(M * N)]

            # At least one
            solver.add_clause(vars_for_cell)

            # At most one
            for t1 in range(M * N):
                for t2 in range(t1 + 1, M * N):
                    solver.add_clause(
                        [-variables[(t1, i, j)], -variables[(t2, i, j)]]
                    )

# (c) Initial position fixed
solver.add_clause([variables[(0, i0, j0)]])
for i in range(M):
    for j in range(N):
        if (i, j) != (i0, j0):
            solver.add_clause([-variables[(0, i, j)]])

# ------------------------------------------------
# (d) Legal move transitions
# For each time t, from cell (i,j), the next move must be a legal knight move
# ------------------------------------------------
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

for t in range(M * N - 1):
    for i in range(M):
        for j in range(N):
            current_var = variables[(t, i, j)]

            # legal next positions
            next_positions = []
            for di, dj in knight_moves:
                ni, nj = i + di, j + dj
                if 0 <= ni < M and 0 <= nj < N:
                    next_positions.append(variables[(t + 1, ni, nj)])

            # If the knight is at (i,j) at time t,
            # then one of these next positions must hold at time t+1.
            if next_positions:
                clause = [-current_var] + next_positions
                solver.add_clause(clause)
            # Otherwise (no legal moves), that assignment can never start a valid path
            else:
                solver.add_clause([-current_var])

# ------------------------------------------------
# 3. Solve with Glucose
# ------------------------------------------------
is_sat = solver.solve()

# Prepare an empty solution grid
solution = [[-1 for _ in range(N)] for _ in range(M)]

if is_sat:
    model = (
        solver.get_model()
    )  # list of integers: positive => True, negative => False

    # Fill solution matrix: solution[i][j] = time index
    for (t, i, j), var in variables.items():
        if var in model:  # variable evaluated to True
            solution[i][j] = t
