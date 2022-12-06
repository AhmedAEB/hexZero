import src.Board as Board

class Game:
    # Returns a blank board
    def get_new_board(self, board_size=11):
        board = Board(board_size)
        return board

    def get_legal_moves(self, agent):
        return agent._choices

    def get_board_size(self, agent):
        return agent._board_size

    def get_action_size(self, agent):
        board_size = self.get_board_size(agent)
        return board_size * board_size + 1
