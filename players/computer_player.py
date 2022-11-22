from players.player import Player
import random

class ComputerPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def get_next_move(self, chessboard):
        return random.choice(chessboard.get_player_possible_moves(self.is_white))

    def get_promoting_choice(self):
        return 'Q'