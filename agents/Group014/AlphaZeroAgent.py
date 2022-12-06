import socket
from random import choice
from time import sleep
import numpy as np

from src14.Game import Game
from src14.Board import Board
from src14.MCTS import MCTS
from src14.NeuralNet import NeuralNet as NNet


class AlphaZeroAgent():
    """This class describes the default Hex agent. It will randomly send a
    valid move at each turn, and it will choose to swap with a 50% chance.
    """

    HOST = "127.0.0.1"
    PORT = 1234

    def run(self):
        """A finite-state machine that cycles through waiting for input
        and sending moves.
        """
        
        self._args = {'numMCTSSims': 50, 'cpuct':1.0}
        
        self._board_size = 0
        self._colour = ""
        self._turn_count = 1
        self._choices = []
        
        self._board = None
        self._game = None
        self._NN = None
        self._MCTS = None
        self._curPlayer = 1
        
        states = {
            1: AlphaZeroAgent._connect,
            2: AlphaZeroAgent._wait_start,
            3: AlphaZeroAgent._make_move,
            4: AlphaZeroAgent._wait_message,
            5: AlphaZeroAgent._close
        }

        res = states[1](self)
        while (res != 0):
            res = states[res](self)

    def _connect(self):
        """Connects to the socket and jumps to waiting for the start
        message.
        """
        
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.connect((AlphaZeroAgent.HOST, AlphaZeroAgent.PORT))

        return 2

    def _wait_start(self):
        """Initialises itself when receiving the start message, then
        answers if it is Red or waits if it is Blue.
        """
        
        data = self._s.recv(1024).decode("utf-8").strip().split(";")
        if (data[0] == "START"):
            self._board_size = int(data[1])
            for i in range(self._board_size):
                for j in range(self._board_size):
                    self._choices.append((i, j))
            self._colour = data[2]
            
            self._game = Game(self._board_size)
            self._board = self._game.getInitBoard()
            self._NN = NNet(self._game)
            self._MCTS = MCTS(self._game, self._NN, 1, self._args)
            self._curPlayer = 1

            if (self._colour == "R"):
                return 3
            else:
                return 4

        else:
            print("ERROR: No START message received.")
            return 0

    def _make_move(self):
        """Makes a random valid move. It will choose to swap with
        a coinflip.
        """
        board = self._game.getCanonicalForm(self._board, self._curPlayer)
        
        action = np.argmax(self._MCTS.getActionProb(board, temp=0))
        valids = self._game.getValidMoves(self._board, 1)
        
        board, self._curPlayer = self._game.getNextState(self._board, self._curPlayer, action)
        
        if (action == self._game.n ** 2):
            msg = "SWAP\n"
        else:
            move = (int(action / self.n), action % self.n)
            msg = f"{move[0]},{move[1]}\n"
        
        self._s.sendall(bytes(msg, "utf-8"))

        return 4

    def _wait_message(self):
        """Waits for a new change message when it is not its turn."""

        self._turn_count += 1

        data = self._s.recv(1024).decode("utf-8").strip().split(";")
        if (data[0] == "END" or data[-1] == "END"):
            return 5
        else:

            if (data[1] == "SWAP"):
                self._colour = self.opp_colour()
                action = self._game.n ** 2
            else:
                x, y = data[1].split(",")
                action = int(x) * self._game.n + int(y)
                
            self._board, self._curPlayer = self._game.getNextState(self._board, self._curPlayer, action)

            if (data[-1] == self._colour):
                return 3

        return 4

    def _close(self):
        """Closes the socket."""

        self._s.close()
        return 0

    def opp_colour(self):
        """Returns the char representation of the colour opposite to the
        current one.
        """
        
        if self._colour == "R":
            return "B"
        elif self._colour == "B":
            return "R"
        else:
            return "None"


if (__name__ == "__main__"):
    agent = AlphaZeroAgent()
    agent.run()
