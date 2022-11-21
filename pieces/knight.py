import pygame
from pieces.piece import Piece

class Knight(Piece):
    def __init__(self, is_white):
        if is_white:
            self.sprite = pygame.image.load('images/whiteknight.png').convert_alpha()
        else:
            self.sprite = pygame.image.load('images/blackknight.png').convert_alpha()
        Piece.__init__(self=self,is_white=is_white)

    def get_possible_moves(self, chessboard, pos):
        possible_moves = []

        i = pos[0]-1
        j = pos[1]-2
 
        if i >= 0 and j >= 0 and i < len(chessboard) and  j < len(chessboard[i]):
            if chessboard[i][j] == 0:
                possible_moves.append((i,j))
            else:
                if self.is_white ^ chessboard[i][j].is_white:
                    possible_moves.append((i,j))

        i = pos[0]+1
        j = pos[1]-2

        if i >= 0 and j >= 0 and i < len(chessboard) and  j < len(chessboard[i]):
            if chessboard[i][j] == 0:
                possible_moves.append((i,j))
            else:
                if self.is_white ^ chessboard[i][j].is_white:
                    possible_moves.append((i,j))
        
        i = pos[0]+2
        j = pos[1]-1

        if i >= 0 and j >= 0 and i < len(chessboard) and  j < len(chessboard[i]):
            if chessboard[i][j] == 0:
                possible_moves.append((i,j))
            else:
                if self.is_white ^ chessboard[i][j].is_white:
                    possible_moves.append((i,j))

        i = pos[0]+2
        j = pos[1]+1

        if i >= 0 and j >= 0 and i < len(chessboard) and  j < len(chessboard[i]):
            if chessboard[i][j] == 0:
                possible_moves.append((i,j))
            else:
                if self.is_white ^ chessboard[i][j].is_white:
                    possible_moves.append((i,j))

        i = pos[0]-2
        j = pos[1]-1

        if i >= 0 and j >= 0 and i < len(chessboard) and  j < len(chessboard[i]):
            if chessboard[i][j] == 0:
                possible_moves.append((i,j))
            else:
                if self.is_white ^ chessboard[i][j].is_white:
                    possible_moves.append((i,j))

        i = pos[0]-2
        j = pos[1]+1

        if i >= 0 and j >= 0 and i < len(chessboard) and  j < len(chessboard[i]):
            if chessboard[i][j] == 0:
                possible_moves.append((i,j))
            else:
                if self.is_white ^ chessboard[i][j].is_white:
                    possible_moves.append((i,j))
        
        i = pos[0]-1
        j = pos[1]+2
 
        if i >= 0 and j >= 0 and i < len(chessboard) and  j < len(chessboard[i]):
            if chessboard[i][j] == 0:
                possible_moves.append((i,j))
            else:
                if self.is_white ^ chessboard[i][j].is_white:
                    possible_moves.append((i,j))

        i = pos[0]+1
        j = pos[1]+2

        if i >= 0 and j >= 0 and i < len(chessboard) and  j < len(chessboard[i]):
            if chessboard[i][j] == 0:
                possible_moves.append((i,j))
            else:
                if self.is_white ^ chessboard[i][j].is_white:
                    possible_moves.append((i,j))

        return possible_moves
