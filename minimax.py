# Minimax with Functional Programming in Python

from functools import reduce

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
        ) else "X"

    # position -> listof position
    def moves(self):
        moves = []
        for i, row in enumerate(self.pos):
            for j, cell in enumerate(row):
                if cell == " ":
                    new_move = [r[:] for r in self.pos]
                    new_move[i][j] = self.player()
                    moves.append(Position(new_move))

        return moves
                    

pos = Position()
print(pos)
print(f"pos.player(): {pos.player()}")
for move in pos.moves():
    print(f"{move}\n")
