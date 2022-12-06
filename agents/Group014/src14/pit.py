import Arena
from MCTS import MCTS
from Game import Game
from NeuralNet import NeuralNet as NNet

import numpy as np

class HumanPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        # display(board)
        #print(board)
        valid = self.game.getValidMoves(board, 1)
        for i in range(len(valid)):
            if valid[i]:
                if i == self.game.n * self.game.n:
                    print("-1 -1 (swap)")
                else:
                    print(int(i/self.game.n), int(i%self.game.n))
        while True:
            a = input()

            x,y = [int(x) for x in a.split(' ')]
            a = self.game.n * x + y if x!= -1 else self.game.n ** 2
            if valid[a]:
                break
            else:
                print('Invalid')

        return a

g = Game(11)
hp = HumanPlayer(g).play
nn = NNet(g)

args1 = {'numMCTSSims': 50, 'cpuct':1.0}
mcts1 = MCTS(g, nn, args1)
nnp = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

arena = Arena.Arena(nnp, hp, g, display=Game.display)

print(arena.playGames(2, verbose=True))