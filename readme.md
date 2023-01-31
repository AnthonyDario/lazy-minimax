# Minimax Algorithm With Lazy Programming in Python
---

This is an implementation of the minimax algorithm implemented with lazy
programming in python. The implementation follows John Hughe's paper "Why
Functional Programming Matters" and uses the streams and numerical methods
implementation from Paul Downen's "Numerical Methods with Functional
Programming".

This branch uses streams to implement the list of descendents of a node in the
tree. This allows the descendents to be evaluated lazily but ends up costing in
runtime, most likely due to the overhead of the specific way the lazy
evaluation is implemented here.
