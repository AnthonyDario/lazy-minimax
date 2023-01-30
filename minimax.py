# Minimax with Functional Programming in Python

import sys
from functools import reduce
from nmfp_template import Stream, Map, Repeat


# Helper streams
# ------------------------------------
emptystream = Repeat(None)

class FiniteStream(Stream):
    def __init__(self, lst):
        self.lst = lst

    def head(self): return self.lst[0]
    def tail(self): return FiniteStream(self.lst[1:]) if len(self.lst) > 1 else emptystream

def min_stream(s):
    if s.head() is None: return None

    val = 10000
    for item in s:
        if item is None: return val         # End of the stream
        val = val if val < item else item

def max_stream(s):
    if s.head() is None: return None

    val = -10000
    for item in s:
        if item is None: return val         # End of the stream
        val = val if val > item else item

# Tic-tac-toe
# ------------------------------------

# A position in tic-tac-toe
class Position:
    def __init__(self, pos=None):
        if pos:
            self.pos = pos
        else:
            self.pos = [[" " for x in range(3)] for y in range(3)]

    #  X|O|
    #  -+-+-
    #   | |
    #  -+-+-
    #   | |
    def __repr__(self):
        strings = [[cell for cell in row] for row in self.pos]
        rows = ["|".join(row) for row in strings]
        return "\n-+-+-\n".join(rows)

    def move(self, i, j):
        new_move = [r[:] for r in self.pos]
        new_move[i][j] = self.player()
        return Position(new_move)
    
    def player(self):
        return "X" if sum(
            [sum([0 if cell == " " else 1 for cell in row]) 
            for row in self.pos]
        ) % 2 == 0 else "O"

# Position -> position stream
class Moves(Stream):
    def __init__(self, pos, row=0, col=0):
        self.pos = pos
        self.row = row
        self.col = col

    def head(self): 
        if self.pos is None: return None
        return self.pos.move(self.row, self.col)

    def tail(self):
        if self.pos is None: return Repeat(EmptyTree)

        col = (self.col + 1) % 3
        row = self.row + 1 if col == 0 else self.row

        while row < 3 and self.pos.pos[row][col] != " ":
            col = (col + 1) % 3
            row = row + 1 if col == 0 else row
        
        if row >= 3: return emptystream

        return Moves(self.pos, row, col)

def static(pos):
    if pos is None: return None

    rows = [0, 0, 0]
    cols = [0, 0, 0]
    diag = [0, 0]

    check_three = lambda x: x / 3 if x == 3 or x == -3 else 0

    for i, row in enumerate(pos.pos):
        for j, cell in enumerate(row):
            val = 1 if cell == "X" else 0 if cell == " " else -1
            rows[i] = rows[i] + val
            cols[j] = cols[j] + val

            if i - j == 0: diag[0] = diag[0] + val
            if i + j == 2: diag[1] = diag[1] + val

        if rows[i] == 3 or rows[i] == -3: return rows[i] / 3

    for col in cols:
        if col == 3 or col == -3: return col / 3

    for d in diag:
        if d == 3 or d == -3: return d / 3

    return 0

# Trees
# ------------------------------------
class Tree:
    def __repr__(self):
        curr   = [repr(self.node())]
        childs = ["\n\t" + repr(child.node()).replace("\n", "\n\t") 
                  for child in self.desc().take(3)]
        return "\n".join(curr + childs) + "\n..."

class RepTree(Tree):
    def __init__(self, a, f):
        self.a = a
        self.f = f

    def node(self): return self.a
    def desc(self): return Map(self.f(self.a), lambda x: RepTree(x, self.f))

class MapTree(Tree):
    def __init__(self, tree, f):
        self.tree = tree
        self.trans = f

    def node(self): return self.trans(self.tree.node())
    def desc(self): return Map(self.tree.desc(), lambda x: MapTree(x, self.trans))

class Prune(Tree):
    def __init__(self, tree, depth):
        self.tree = tree
        self.depth = depth

    def node(self): return self.tree.node()
    def desc(self):
        if self.depth == 0: return Repeat(EmptyTree())
        return Map(self.tree.desc(), lambda x: Prune(x, self.depth - 1))

class EmptyTree(Tree):
    def node(self): return None
    def desc(self): return Repeat(EmptyTree())

# Method for traversing the tree
def descend(tree):
    for d in tree.desc():
        if d.node() is None: return
        print(d)

# Decomposed maximium and minimum functions
# ------------------------------------
def maximize(tree):
    return max_stream(maxi)

def maxi(tree):
    if tree.desc().head().node() is None: return Repeat(tree.node(), lambda x: None)
    return Map(Map(tree.desc(), lambda x: mini(x)), lambda x: 0 if x is None else min_stream(x))

def minimize(tree):
    return min_stream(mini)

def mini(tree):
    if tree.desc().head().node() is None: return Repeat(tree.node(), lambda x: None)
    return Map(Map(tree.desc(), lambda x: maxi(x)), lambda x: 0 if x is None else max_stream(x))

#def omit(pot, xs):
#    if xs.head() is None: return emptystream
#    elif minleq(xs.head(), pot): return omit(pot, xs.tail())
#    else: return [min(xs[0])].append(omit(min(xs[0]), xs[1:]))
#
#
#    #if len(xs) == 0: return []
#    #elif minleq(xs[0], pot): return omit(pot, xs[1:])
#    #else: return [min(xs[0])].append(omit(min(xs[0]), xs[1:]))
#
#def minleq(ns, pot):
#    if len(ns) == 0: return false
#    elif ns[0] <= pot: return true
#    else: return minleq(ns[1:], pot)

# Optimizations
# ------------------------------------
class HighFirst(Tree):
    def __init__(self, tree):
        self.tree = tree

    def node(self): return self.tree.node()
    def desc(self): 
        lows = [LowFirst(t) for t in self.tree.desc()]
        return sorted(lows, reverse=True, key=lambda x: x.node())

class LowFirst(Tree):
    def __init__(self, tree):
        self.tree = tree

    def node(self): return self.tree.node()
    def desc(self): 
        highs = [HighFirst(t) for t in self.tree.desc()]
        return sorted(highs, reverse=False, key=lambda x: x.node())

def red_tree(f, g, a, tree):
    return f(tree.node(), red_tree_prime(f, g, a, tree.desc()))

def red_tree_prime(f, g, a, trees):
    if trees == []: return a
    return g(red_tree(f, g, a, trees[0]), red_tree_prime(f, g, a, trees[1:]))

gametree = RepTree(Position(), lambda x: Moves(x),)

# minimax: 90 seconds!
evaluation = max_stream(maxi(MapTree(Prune(gametree, 8), static)))

# High first, sort the descendents:
#evaluation = max_stream(maxi(HighFirst(MapTree(Prune(gametree, 2), static))))

# Only the three Best Moves:
class TakeTree(Tree):
    def __init__(self, n, tree):
        self.tree = tree
        self.n = n

    def node(self): return self.tree.node()
    def desc(self): return self.tree.desc()[self.n:]

#evaluation = max_stream(maxi(TakeTree(3, HighFirst(MapTree(Prune(gametree, 8), static)))))

print(f"evaluation: {evaluation}")
