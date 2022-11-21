import pygame
from pieces.piece import Piece

class Rook(Piece):
    def __init__(self, is_white, sprite):
        Piece.__init__(self=self,is_white=is_white,sprite=sprite)
        self.material_value = 5

    def get_code(self):
        l = 'R'
        if not self.is_white:
            l = l.lower()
        return l

    def move(self):
        self.can_castle = False

    def get_possible_moves(self, chessboard, pos):
        possible_moves = []

        for i in range(pos[1]-1, -1, -1):
            if chessboard[pos[0]][i] == 0:
                possible_moves.append((pos[0], i))
            else:
                if self.is_white ^ chessboard[pos[0]][i].is_white:
                    possible_moves.append((pos[0], i))
                break

        for i in range(pos[1]+1, len(chessboard[pos[1]])):
            if chessboard[pos[0]][i] == 0:
                possible_moves.append((pos[0], i))
            else:
                if self.is_white ^ chessboard[pos[0]][i].is_white:
                    possible_moves.append((pos[0], i))
                break

        for i in range(pos[0]+1, len(chessboard)):
            if chessboard[i][pos[1]] == 0:
                possible_moves.append((i, pos[1]))
            else:
                if self.is_white ^ chessboard[i][pos[1]].is_white:
                    possible_moves.append((i, pos[1]))
                break

        for i in range(pos[0]-1, -1, -1):
            if chessboard[i][pos[1]] == 0:
                possible_moves.append((i, pos[1]))
            else:
                if self.is_white ^ chessboard[i][pos[1]].is_white:
                    possible_moves.append((i, pos[1]))
                break
        

        return possible_moves
