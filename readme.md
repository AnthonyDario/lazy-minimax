# Minimax Algorithm With Lazy Programming in Python

This is an implementation of the minimax algorithm implemented with lazy
programming in python. The implementation follows John Hughe's paper "Why
Functional Programming Matters" and uses the streams and numerical methods
implementation from Paul Downen's "Numerical Methods with Functional
Programming".

This branch uses python lists when returning the descendents of a node. This
is fairly reasonable for the tic-tac-toe case since the there are not more than
9 potential descendents in the tree. However for a game with more branching
this could get unwieldy. Check out the "streams" branch to see an
implementation with lazy streams.
