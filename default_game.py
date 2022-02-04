from chessboard import Chessboard
from pieces.piece import Piece
from pieces.king import King
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.queen import Queen

def reset_board_to_default_game(board):
    # Pawns
    for i in range(8):
        board.add_piece((i,1), Pawn(False))
        board.add_piece((i,6), Pawn(True))

    # Rooks
    board.add_piece((0,0),Rook(False))
    board.add_piece((7,0),Rook(False))
    board.add_piece((0,7),Rook(True))
    board.add_piece((7,7),Rook(True))
    
    # Knights
    board.add_piece((1,0),Knight(False))
    board.add_piece((6,0),Knight(False))
    board.add_piece((1,7),Knight(True))
    board.add_piece((6,7),Knight(True))

    # Bishops
    board.add_piece((2,0),Bishop(False))
    board.add_piece((5,0),Bishop(False))
    board.add_piece((2,7),Bishop(True))
    board.add_piece((5,7),Bishop(True))

    # Queens
    board.add_piece((3,0),Queen(False))
    board.add_piece((3,7),Queen(True))

    # Kings
    board.add_piece((4,0),King(False))
    board.add_piece((4,7),King(True))
