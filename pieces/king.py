import pygame
from pieces.piece import Piece

class King(Piece):
    def __init__(self, is_white):
        Piece.__init__(self=self,is_white=is_white)
        if is_white:
            self.sprite = pygame.image.load('images/whiteking.png').convert_alpha()
        else:
            self.sprite = pygame.image.load('images/blackking.png').convert_alpha()
        self.is_king = True

        self.can_castle = True

    def move(self):
        self.can_castle = False

    def get_possibile_moves(self, chessboard, pos):
        possibile_moves = []

        for i in range(pos[0]-1, pos[0]+2):
            for j in range(pos[1]-1, pos[1]+2):
                if i >= 0 and j >= 0 and i < len(chessboard) and j < len(chessboard[0]):
                    # I'm not checking if the new position is safe
                    if chessboard[i][j] == 0:
                        possibile_moves.append((i,j))
                    else:
                        if chessboard[i][j].is_white != self.is_white:
                            possibile_moves.append((i,j))

        return possibile_moves

    def render(self, screen, pos):
        sprite_rect = self.sprite.get_rect(center=pos)
        screen.blit(self.sprite, sprite_rect)

