from players.player import Player

class LocalPlayer(Player):
    def __init__(self):
        super().__init__()

    def get_next_move(self, chessboard):
        super().get_next_move(chessboard)
        m,self.next_move = self.next_move,None
        return m

    def set_next_move(self, starting_cell, destination_cell):
        self.next_move = (starting_cell, destination_cell)

    def set_promoting_choice(self, choice):
        self.promoting_choice = choice

    def get_promoting_choice(self):
        super().get_promoting_choice()
        c,self.promoting_choice = self.promoting_choice,None
        return c