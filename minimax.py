# Minimax with Functional Programming in Python
#
# Based on John Hughes paper "Why Functional Programming Matters" and Paul
# Downen's "Numerical Methods with Functional Programming in Python"
#
# Descendents of trees are implemented using standard python lists. This is not a
# fully lazy implementation, see the "streams" branch for a lazier implementation.

# ------------------------------------
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

# position -> listof position
def moves(pos):
    if pos == None or static(pos) != 0: return []

    next_moves = []
    for i, row in enumerate(pos.pos):
        for j, cell in enumerate(row):
            if cell == " ":
                new_move = [r[:] for r in pos.pos]
                new_move[i][j] = pos.player()
                next_moves.append(Position(new_move))

    return next_moves
    
# Statically evaluate tic-tac-toe positions. 1 if 'X' has won, -1 if 'O' has
# won, 0 otherwise
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

        if rows[i] == 3 or rows[i] == -3: 
            #print(f'returning: rows[i] / 3: {rows[i] / 3}')
            return rows[i] / 3

    for col in cols:
        if col == 3 or col == -3: 
            #print(f'returning: col / 3: {col / 3}')
            return col / 3

    for d in diag:
        if d == 3 or d == -3: 
            #print(f'returning: d / 3: {d / 3}')
            return d / 3

    return 0

# ------------------------------------
# Trees
# ------------------------------------
class Tree:
    def __repr__(self):
        curr   = [repr(self.node())]
        childs = ["\n\t" + repr(child.node()).replace("\n", "\n\t") 
                  for child in self.desc()[:3]]
        return "\n".join(curr + childs) + "\n..."

# Repeat the function on each node to get the descendents
class RepTree(Tree):
    def __init__(self, a, f):
        self.a = a
        self.f = f

    def node(self): return self.a
    def desc(self): return [RepTree(a, self.f) for a in self.f(self.a)]

# Apply function f to every node in the tree
class MapTree(Tree):
    def __init__(self, tree, f):
        self.tree = tree
        self.trans = f

    def node(self): return self.trans(self.tree.node())
    def desc(self): return [MapTree(t, self.trans) for t in self.tree.desc()]

# A tree with a set depth
class Prune(Tree):
    def __init__(self, tree, depth):
        self.tree = tree
        self.depth = depth

    def node(self): return self.tree.node()
    def desc(self):
        if self.depth == 0: return []
        return [Prune(t, self.depth - 1) for t in self.tree.desc()]

# Sort the descendents high to low
class HighFirst(Tree):
    def __init__(self, tree):
        self.tree = tree

    def node(self): return self.tree.node()
    def desc(self): 
        lows = [LowFirst(t) for t in self.tree.desc()]
        return sorted(lows, reverse=True, key=lambda x: x.node())

# Sort the descendents low to high
class LowFirst(Tree):
    def __init__(self, tree):
        self.tree = tree

    def node(self): return self.tree.node()
    def desc(self): 
        highs = [HighFirst(t) for t in self.tree.desc()]
        return sorted(highs, reverse=False, key=lambda x: x.node())

# Take only the first n descendents of the tree
class TakeTree(Tree):
    def __init__(self, n, tree):
        self.tree = tree
        self.n = n

    def node(self): return self.tree.node()
    def desc(self): return self.tree.desc()[self.n:]

# ------------------------------------
# Decomposed maximium and minimum functions
# ------------------------------------

# See "Why functional programming matters for an in-depth explanation of these
# functions
def maximize(tree): return max(maxi)

def maxi(tree):
    if len(tree.desc()) == 0: return [tree.node()]
    return [min(ms) for ms in [mini(t) for t in tree.desc()]]

def minimize(tree):
    return min(mini)

def mini(tree):
    if len(tree.desc()) == 0: return [tree.node()]
    return [max(ms) for ms in [maxi(t) for t in tree.desc()]]

def mapmin(xs):
    return [min(xs[0])].append(omit(min(xs[0]), xs[1:]))

def omit(pot, xs):
    if len(xs) == 0: return []
    elif minleq(xs[0], pot): return omit(pot, xs[1:])
    else: return [min(xs[0])].append(omit(min(xs[0]), xs[1:]))

def minleq(ns, pot):
    if len(ns) == 0: return false
    elif ns[0] <= pot: return true
    else: return minleq(ns[1:], pot)

# ------------------------------------
# Optimizations
# ------------------------------------

gametree = RepTree(Position(), moves)

# minimax: 3.28
#evaluation = max(maxi(MapTree(Prune(gametree, 8), static)))

# High first, sort the descendents: 5.34 seconds
#evaluation = max(maxi(HighFirst(MapTree(Prune(gametree, 8), static))))

# Only the three Best Moves: 3.59
evaluation = max(maxi(TakeTree(3, HighFirst(MapTree(Prune(gametree, 8), static)))))

print(f"evaluation: {evaluation}")
