from __future__ import print_function
import sys
sys.path.append('..')
from Board import Board
import numpy as np

I_DISPLACEMENTS = [-1, -1, 0, 1, 1, 0]
J_DISPLACEMENTS = [0, 1, 1, 0, -1, -1]

class Game():
    def __init__(self, n=15):
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions 
        return self.n * self.n + 1 #(for swap)

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        b = Board(self.n)
        b.pieces = np.copy(board)
        
        if action == self.n * self.n:
            b.pieces *= -1
            b.pieces[-1] = 1
        else:
            move = (int(action / self.n), action % self.n)
            b.execute_move(move, b.getNextPlayer())
        
        return (b.pieces, -player)

    # modified
    def getValidMoves(self, board, _):
        # return a fixed size binary vector
        valids = [0] * self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves = b.get_legal_moves(1)
        if not b[-1][-1] and b.getNPlaced() == 1:
            valids[-1] = 1
        for x, y in legalMoves:
            valids[self.n * x + y] = 1
        return np.array(valids)

    def DFS(self, board, player, x, y, visited):
        if x < 0 or x >= self.n or y < 0 or y >= self.n:
            return False
        if board[x][y] != player:
            return False
        if visited[x][y]:
            return False
        visited[x][y] = True
        if (player == 1 and x == self.n - 1) or (player == -1 and y == self.n - 1):
            return True
        return any(self.DFS(board, player, x + I_DISPLACEMENTS[i], y + J_DISPLACEMENTS[i], visited) for i in range(6))

    # modified
    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        swap = board[-1][-1]
        
        board = np.copy(board)
        
        if swap:
            board *= -1
            player *= -1
        
        board = np.delete(board, self.n, 0)
        # n = self.n_in_row

        # Check if player 1 has a winning path from top to bottom
        for i in range(self.n):
            if self.DFS(board, 1, 0, i, [[False] * self.n for _ in range(self.n)]):
                return player
                
        # Check if player 2 has a winning path from left to right
        for i in range(self.n):
            if self.DFS(board, -1, i, 0, [[False] * self.n for _ in range(self.n)]):
                return player * -1

        return 0
    

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        b = board.copy()
        #b[self.n][0] *= -1
        return b # Rules for hex are different (inverting results in false wins)

    # modified
    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n**2 + 1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []
        #print(board)
        #last_row = board[self.n]
        swap = board[-1][-1]
        
        if swap:
            board *= -1
            
        #print(last_row, "L")
        board = np.delete(board, self.n, 0)
        
        l += [(board, pi)]
        l += [(np.fliplr(board), list(np.fliplr(pi_board).ravel()) + [pi[-1]])]
        l += [(np.flipud(board), list(np.flipud(pi_board).ravel()) + [pi[-1]])]
        l += [(np.flipud(np.fliplr(board)), list(np.flipud(np.fliplr(pi_board)).ravel()) + [pi[-1]])]
        #print(l)
        return l

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tostring()

    @staticmethod
    def display(board):
        n = board.shape[0]-1
        
        board = np.copy(board)
        
        swap = board[-1][-1]
        
        if swap: board *= -1

        for y in range(n):
            print(y, "|", end="")
        print("")
        print(" -----------------------")
        for y in range(n):
            print(" "*y, y, "|", end="")    # print the row #
            for x in range(n):
                piece = board[y][x]    # get the piece to print
                if piece == -1:
                    print("B ", end="")
                elif piece == 1:
                    print("R ", end="")
                else:
                    if x == n:
                        print("-", end="")
                    else:
                        print("- ", end="")
            print("|")
        print("   -----------------------")
        print("TURN: ", board[n][n-1])
