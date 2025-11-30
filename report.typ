#set page("a4")

#set par(
  spacing: 1.5em,
  justify: true,
)

#set document(
  title: [Logic for Computer Science],
  description: [Project Report],
  author: "Alexandru Dobre",
  date: datetime(
    year: 2025,
    month: 11,
    day: 30,
  )
)

#set heading(numbering: "1.1.")
#set enum(numbering: "a)", spacing: 1.5em)

//#title()
#align(center)[
  #text(size: 24pt, weight: "bold")[Logic for Computer Science]

  #text(size: 18pt, style: "italic")[Project Report]

  #text(size: 14pt)[Alexandru Dobre]
  #v(0.3em)
  #text(size: 12pt)[November 30, 2025]
]

= Introduction

This report is about solving the knight's tour problem using a SAT solver.

We define $s$ as the step the knight is in.
For instance, when the knight is in the initial position $(i_0, j_0)$, $s = 0$.
We define the boolean variable $x_(s,i,j)$ which is True iff the knight is in cell $(i, j)$ at step $s$.
The indices range as follows: steps $s in [0, M times N - 1]$, rows $i in [0, M-1]$, and columns $j in [0, N-1]$.

= First Question

We encode the problem using the following constraints:

+ At step $s=0$, the knight must be at the given position $(i_0, j_0)$.
  $ x_(0, i_0, j_0) $

+ For every step $s$, the knight must be in exactly one cell. We split this into two parts:
  - At least one cell:
    $ and.big_(s) ( or.big_(i,j) x_(s,i,j) ) $
  - At most one cell: For every pair of distinct cells, the knight cannot be in both.
    $ and.big_(s) ( and.big_((i,j) != (i',j')) (not x_(s,i,j) or not x_(s,i',j')) ) $

+ The knight can only move according to chess rules. We split this into two parts:
  - For every step $s < M times N - 1$, if the knight is at $(i,j)$, it must move to a valid cell at step $s+1$.
  $ and.big_(s=0)^(M times N - 2) and.big_(i,j) ( not x_(s,i,j) or or.big_("Valid"(i', j')) x_(s+1, i', j') ) $
  - For every step $s > 0$, the knight must have been in a valid cell at step $s-1$.
  $ and.big_(s=1)^(M times N) and.big_(i,j) ( not x_(s,i,j) or or.big_("Valid"(i', j')) x_(s-1, i', j') ) $

+ Every cell $(i,j)$ must be visited at exactly one time step.
  - At least once:
    $ and.big_(i,j) ( or.big_(s) x_(s,i,j) ) $
  - At most once: For any cell, it cannot be visited at two different steps $s$ and $s'$.
    $ and.big_(i,j) ( and.big_(s != s') (not x_(s,i,j) or not x_(s',i,j)) ) $

= Second Question


= Third Question

For each starting position $(i_0, j_0)$, we execute `question1()`.
For each valid solution found from $(i_0, j_0)$, `nb_sol` is incremented and the found solution
is made insatisfiable by negating every $(s, i, j)$ that satisfies it. $forall n in "Model(question1("i_0,j_0,3,4"))"$,
$ or.big_(n > 0) not n $

= Fourth Question

The idea is to iterate through all starting positions $(i, j)$ on the board
and use `question1(3, 4, i, j)` for each starting position.
For each found solution, the 3 symetries are created and stored in a set to exclude possible duplicates.

= Fifth Question

We start at starting position $(i_0, j_0)$ and firstly test if
this starting position outputs a solution by executing `question1()`.
If so, we test the uniqueness of the solution.
If the solution is unique, we only return $(0, i_0, j_0)$.
If there are two or more solutions,
