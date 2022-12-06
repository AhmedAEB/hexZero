class NNet():
    def __init__(self, game, args):
        self.game = game
        self.maxX, self.maxY = game.getBoardSize()
        self.args = args