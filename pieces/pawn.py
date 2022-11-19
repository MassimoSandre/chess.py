import pygame
from pieces.piece import Piece

class Pawn(Piece):
    def __init__(self, is_white):
        Piece.__init__(self=self,is_white=is_white)
        if is_white:
            self.sprite = pygame.image.load('images/whitepawn.png').convert_alpha()
        else:
            self.sprite = pygame.image.load('images/blackpawn.png').convert_alpha()
        self.is_promotable = True

    def get_possibile_moves(self, chessboard, pos):
        possibile_moves = []

        if not self.is_white:
            i = pos[0]
            j = pos[1]-1
            if i >= 0 and j >= 0 and i < len(chessboard) and  j < len(chessboard[i]):
                if chessboard[i][j] == 0:
                    possibile_moves.append((i,j))
                    j = j - 1
                    if pos[1] == 6 and i >= 0 and j >= 0 and i < len(chessboard) and  j < len(chessboard[i]):
                        if chessboard[i][j] == 0:
                            possibile_moves.append((i,j))
                    j = j + 1


            i = i - 1
            if i >= 0 and j >= 0 and i < len(chessboard) and  j < len(chessboard[i]):
                if chessboard[i][j] != 0:
                    if self.is_white ^ chessboard[i][j].is_white:
                        possibile_moves.append((i,j))

            i = i + 2
            if i >= 0 and j >= 0 and i < len(chessboard) and  j < len(chessboard[i]):
                if chessboard[i][j] != 0:
                    if self.is_white ^ chessboard[i][j].is_white:
                        possibile_moves.append((i,j))
            
        else:
            i = pos[0]
            j = pos[1]+1
            if i >= 0 and j >= 0 and i < len(chessboard) and  j < len(chessboard[i]):
                if chessboard[i][j] == 0:
                    possibile_moves.append((i,j))
                    j = j + 1
                    if pos[1] == 1 and i >= 0 and j >= 0 and i < len(chessboard) and  j < len(chessboard[i]):
                        if chessboard[i][j] == 0:
                            possibile_moves.append((i,j))
                    j = j - 1

            i = i - 1
            if i >= 0 and j >= 0 and i < len(chessboard) and  j < len(chessboard[i]):
                if chessboard[i][j] != 0:
                    if self.is_white ^ chessboard[i][j].is_white:
                        possibile_moves.append((i,j))

            i = i + 2
            if i >= 0 and j >= 0 and i < len(chessboard) and  j < len(chessboard[i]):
                if chessboard[i][j] != 0:
                    if self.is_white ^ chessboard[i][j].is_white:
                        possibile_moves.append((i,j))

        return possibile_moves

    def render(self, screen, pos):
        sprite_rect = self.sprite.get_rect(center=pos)
        screen.blit(self.sprite, sprite_rect)

