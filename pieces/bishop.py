import pygame
from pieces.piece import Piece

class Bishop(Piece):
    def __init__(self, is_white):
        if is_white:
            self.sprite = pygame.image.load('images/whitebishop.png').convert_alpha()
        else:
            self.sprite = pygame.image.load('images/blackbishop.png').convert_alpha()
        Piece.__init__(self=self,is_white=is_white)

    def get_possible_moves(self, chessboard, pos):
        possible_moves = []

        i = pos[0]-1
        j = pos[1]-1

        while i >= 0 and j >= 0:
            if chessboard[i][j] == 0:
                possible_moves.append((i,j))
            else:
                if self.is_white ^ chessboard[i][j].is_white:
                    possible_moves.append((i,j))
                break
            i = i - 1
            j = j - 1

        i = pos[0]+1
        j = pos[1]-1

        while i < len(chessboard) and j >= 0:
            if chessboard[i][j] == 0:
                possible_moves.append((i,j))
            else:
                if self.is_white ^ chessboard[i][j].is_white:
                    possible_moves.append((i,j))
                break
            i = i + 1
            j = j - 1
        
        i = pos[0]+1
        j = pos[1]+1

        while i < len(chessboard) and j < len(chessboard[i]):
            if chessboard[i][j] == 0:
                possible_moves.append((i,j))
            else:
                if self.is_white ^ chessboard[i][j].is_white:
                    possible_moves.append((i,j))
                break
            i = i + 1
            j = j + 1

        i = pos[0]-1
        j = pos[1]+1

        while i >= 0 and j < len(chessboard[i]):
            if chessboard[i][j] == 0:
                possible_moves.append((i,j))
            else:
                if self.is_white ^ chessboard[i][j].is_white:
                    possible_moves.append((i,j))
                break
            i = i - 1
            j = j + 1
        

        return possible_moves

