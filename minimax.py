# Minimax with Functional Programming in Python

from functools import reduce
from nmfp_template import Stream, Map, Repeat


# Helper streams
# ------------------------------------
empty = Repeat(None)

class FiniteStream(Stream):
    def __init__(self, lst):
        self.lst = lst

    def head(self): return self.lst[0]
    def tail(self): return FiniteStream(self.lst[1:]) if len(self.lst) > 1 else empty

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
    
    def player(self):
        return "O" if sum(
            [sum([0 if cell == " " else 1 for cell in row]) 
            for row in self.pos]
        ) % 2 == 0 else "X"

# position -> listof position
def moves(pos):
    if pos == None: return None

    next_moves = []
    for i, row in enumerate(pos.pos):
        for j, cell in enumerate(row):
            if cell == " ":
                new_move = [r[:] for r in pos.pos]
                new_move[i][j] = pos.player()
                next_moves.append(Position(new_move))

    
    return FiniteStream(next_moves) if len(next_moves) > 0 else empty

def static(pos):
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
    def __init__(self, f, a):
        self.a = a
        self.f = Map(f(a), lambda x: RepTree(f, x))

    def node(self): return self.a
    def desc(self): return self.f

class MapTree(Tree):
    def __init__(self, tree, f):
        self.tree = tree
        self.trans = f

    def node(self): return self.trans(self.tree.node())
    def desc(self): return Map(tree.desc, lambda x: MapTree(x, self.trans))

gametree = RepTree(moves, Position())

class Prune(Tree):
    def __init__(self, tree, depth):
        self.tree = tree
        self.depth = depth

    
def prune(depth, tree):
    if depth == 0:
        return tree
    else:
        return tree 


#print(f"tic:\n{tic}\n")
print(f"tac:\n{gametree}\n")
def descend(tree):
    for d in tree.desc():
        if d.node() is None:
            return
        elif static(d.node()) != 0:
            print(d.node())
            print(static(d.node()))
            print()
        else:
            print(f"descending on:\n{d.node()}")
            descend(d)

#descend(gametree)

