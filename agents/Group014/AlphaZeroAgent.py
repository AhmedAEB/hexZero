import socket
from random import choice
from time import sleep
from src.Board import Board
from src.Game import Game

"""

"""


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

        self._board_size = 0
        self._board = Board(board_size=self._board_size)
        self._colour = ""
        self._turn_count = 1
        self._choices = []

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

        print("AZ Agent: Connected to server.")
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

            # Print assigned colour
            print(f"[AZ Agent] Assigned colour: {self._colour}")
            # Print board size X * X
            print(f"[AZ Agent] Board size: {self._board_size} * {self._board_size}")

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

        if (self._turn_count == 2 and choice([0, 1]) == 1):
            msg = "SWAP\n"
        else:
            move = choice(self._choices)
            msg = f"{move[0]},{move[1]}\n"

        # Call get_valid_moves from Game
        game = Game()
        valid_moves = game.get_legal_moves(self)

        # Print out valid moves
        print(f"[AZ Agent] Valid moves: {valid_moves}")

        print(f"[AZ Agent] Making move: {msg[:-1]} as {self._colour}")
        self._s.sendall(bytes(msg, "utf-8"))

        return 4

    def _wait_message(self):
        """Waits for a new change message when it is not its turn."""

        self._turn_count += 1

        data = self._s.recv(1024).decode("utf-8").strip().split(";")

        # Display data from message received
        # print(f"[AZ Agent] Received message: {data}")
        # Display board
        if data[0] == "END" or data[-1] == "END":
            return 5
        else:
            if data[1] == "SWAP":
                self._colour = self.opp_colour()
                print(f"[AZ Agent] Swapped to {self._colour}")
            else:
                x, y = data[1].split(",")
                self._choices.remove((int(x), int(y)))

            if data[-1] == self._colour:
                # Print opponent making move
                print(f"[Opponent] Making move: {data[1]} as {self.opp_colour()}")
                self._board = Board.from_string(data[2], board_size=self._board_size)
                print(f"[AZ Agent] Updated Board:\n{self._board.print_board(bnf=False)}")
                return 3

        if data[0] == "CHANGE":
            self._board = Board.from_string(data[2], board_size=self._board_size)
            print(f"[AZ Agent] Updated Board:\n{self._board.print_board(bnf=False)}")

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


if __name__ == "__main__":
    agent = AlphaZeroAgent()
    agent.run()