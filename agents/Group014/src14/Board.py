class Board():
    def __init__(self, n):
        "Set up initial board configuration."
        self.n = n
        # self.legal_moves = set()
        self.can_swap = True

        # Create the empty board array.
        self.pieces = [None] * (self.n + 1)
        for i in range(self.n + 1):
            self.pieces[i] = [0] * self.n

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.pieces[index]

    def getNPlacedC(self, colour):
        swap = self[-1][-1]
        
        if swap: colour *= -1
        
        count = 0
        # Get all empty locations.
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == colour:
                    count += 1
        return count
    
    def getNPlaced(self):
        count = 0
        # Get all empty locations.
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] != 0:
                    count += 1
        return count
    
    def getNextPlayer(self):
        swap = self[-1][-1]
        
        redPieces = self.getNPlacedC(1)
        bluePieces = self.getNPlacedC(-1)
        
        if swap == 0:
            if redPieces > bluePieces:
                return -1
            else:
                return 1
        else:
            if redPieces > bluePieces:
                return 1
            else:
                return -1

    def get_legal_moves(self, _):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = set()  # stores the legal moves.

        # Get all empty locations.
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == 0:
                    moves.add((x, y))
        return list(moves)

    def has_legal_moves(self):
        """Returns True if has legal move else False
        """
        # Get all empty locations.
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == 0:
                    return True
        return False

    def execute_move(self, move, nextPiece):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=white,-1=black)
        """
        (x, y) = move
        try:
            assert self[x][y] == 0
        except AssertionError:
            print(move, color, self.pieces)
            raise AssertionError
        self[x][y] = nextPiece
        # self.legal_moves.remove(move)
