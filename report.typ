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
We'll need a variable to keep track of the step the program is in.
The variable $s$ (for step) ranges from $0$ to $M times N - 1$.

We now have a way to add clauses to our solver. Each $(s,i,j)$ tuple describes a proposition.
The following proposition means "The knight is in cell (i, j) at step $s$" : $x_((s,i,j))$.
We also map each $(s,i,j)$ to one unique ID with a dictionary.

In this document, $i in [0,M]$ and $j in [0,N]$ and $(i_0,j_0)$ is the starting cell.


= First Question

We define the proposition $x_((s,i,j))$ as true if the knight is in cell $(i, j)$ at step $s$.
We have the following constraints:

+ At step $s=0$, the knight is at $(i_0, j_0)$.
  $ x_((0, i_0, j_0)) $

+ At every step $s$, the knight must be in exactly one cell.
  This requires two clauses: "at least one" and "at most one".
  $ and.big_(s) (or.big_(i,j) x_((s,i,j))) quad "and" quad and.big_(s) (and.big_((i,j) != (i',j')) (not x_((s,i,j)) or not x_((s,i',j')))) $

+ If the knight is at $(i,j)$ at step $s$, it must be at a valid neighbor $(i', j') in "Moves"(i,j)$ at step $s+1$.
  $ and.big_(s, i, j) (x_((s,i,j)) arrow.r.double or.big_((i', j') in "Moves"(i,j)) x_((s+1, i', j'))) $

+ Every cell $(i,j)$ must be occupied at exactly one time step $s$.
  $ and.big_(i,j) (or.big_(s) x_((s,i,j))) quad "and" quad and.big_(i,j) (and.big_(s != s') (not x_((s,i,j)) or not x_((s',i,j)))) $

= Second Question


= Third Question

To count the number of solutions, we use a loop with Blocking Clauses:
#set enum(numbering: "1.", spacing: 1.5em)
1. Run the SAT solver.
2. If a model (solution) $S$ is found, increment the counter.
3. Add a new clause to the solver that invalidates $S$. The clause is the negation of the conjunction of all true variables in $S$:
   $ not (and.big_((s,i,j) in S) x_((s,i,j))) equiv or.big_((s,i,j) in S) not x_((s,i,j)) $
4. Repeat until the solver returns "UNSAT".


= Fourth Question


= Fifth Question
