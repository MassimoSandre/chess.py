from chessboard import Chessboard
from pieces.piece import Piece
from pieces.king import King
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.queen import Queen
WHITE = True
BLACK = False

def reset_board_to_default_game(board):
    # Pawns
    for i in range(8):
        board.add_piece((i,1), Pawn(WHITE))
        board.add_piece((i,6), Pawn(BLACK))

    # Rooks
    board.add_piece((0,0),Rook(WHITE))
    board.add_piece((7,0),Rook(WHITE))
    board.add_piece((0,7),Rook(BLACK))
    board.add_piece((7,7),Rook(BLACK))
    
    # Knights
    board.add_piece((1,0),Knight(WHITE))
    board.add_piece((6,0),Knight(WHITE))
    board.add_piece((1,7),Knight(BLACK))
    board.add_piece((6,7),Knight(BLACK))

    # Bishops
    board.add_piece((2,0),Bishop(WHITE))
    board.add_piece((5,0),Bishop(WHITE))
    board.add_piece((2,7),Bishop(BLACK))
    board.add_piece((5,7),Bishop(BLACK))

    # Kings
    board.add_piece((3,0),King(WHITE))
    board.add_piece((3,7),King(BLACK))

    # Queens
    board.add_piece((4,0),Queen(WHITE))
    board.add_piece((4,7),Queen(BLACK))
