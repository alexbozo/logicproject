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

We define the boolean variable $x_(s,i,j)$ which is true if the knight is in cell $(i, j)$ at step $s$.
The indices range as follows: steps $s in [0, M times N - 1]$, rows $i in [0, M-1]$, and columns $j in [0, N-1]$.

We encode the problem using the following constraints derived directly from the CNF clauses in our code:

+ Initial Position: At step $s=0$, the knight must be at the given position $(i_0, j_0)$.
  $ x_(0, i_0, j_0) $

+ Valid Position at Each Step: For every step $s$, the knight must be in exactly one cell. We split this into two parts:
  - At least one cell:
    $ and.big_(s) ( or.big_(i,j) x_(s,i,j) ) $
  - At most one cell (Pairwise Exclusion): For every pair of distinct cells, the knight cannot be in both.
    $ and.big_(s) ( and.big_((i,j) != (i',j')) (not x_(s,i,j) or not x_(s,i',j')) ) $

+ Legal Moves (Transitions): For every step $s < M times N - 1$, if the knight is at $(i,j)$, it must move to a valid neighbor in the next step.
  $ and.big_(s=0)^(M N - 2) and.big_(i,j) ( not x_(s,i,j) or or.big_((i', j') in "Moves"(i,j)) x_(s+1, i', j') ) $
  This is equivalent to the implication $x_(s,i,j) => or.big x_(s+1, i', j')$.

+ Visit Each Cell Exactly Once: Every cell $(i,j)$ must be visited at exactly one time step.
  - At least once:
    $ and.big_(i,j) ( or.big_(s) x_(s,i,j) ) $
  - At most once (Pairwise Exclusion): For any cell, it cannot be visited at two different steps $s$ and $s'$.
    $ and.big_(i,j) ( and.big_(s != s') (not x_(s,i,j) or not x_(s',i,j)) ) $

= Second Question


= Third Question


= Fourth Question


= Fifth Question
