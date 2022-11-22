class Player:
    def __init__(self):
        self.next_move = None
        self.promoting_choice = None

    def set_color(self, is_white):
        self.is_white = is_white

    def get_next_move(self, chessboard):
        return None

    def get_promoting_choice(self):
        return None