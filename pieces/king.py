import pygame
from pieces.piece import Piece

class King(Piece):
    def __init__(self, is_white):
        if is_white:
            self.sprite = pygame.image.load('images/whiteking.png').convert_alpha()
        else:
            self.sprite = pygame.image.load('images/blackking.png').convert_alpha()
        Piece.__init__(self=self,is_white=is_white)

        self.is_king = True

        self.check = False
        

    def move(self):
        self.can_castle = False

    def get_possible_moves(self, chessboard, pos):
        possible_moves = []

        for i in range(pos[0]-1, pos[0]+2):
            for j in range(pos[1]-1, pos[1]+2):
                if i >= 0 and j >= 0 and i < len(chessboard) and j < len(chessboard[0]):
                    # I'm not checking if the new position is safe
                    if chessboard[i][j] == 0:
                        possible_moves.append((i,j))
                    else:
                        if chessboard[i][j].is_white != self.is_white:
                            possible_moves.append((i,j))


        
        # castling
        if self.can_castle and not self.check:
            
            if chessboard[0][pos[1]] != 0 and chessboard[0][pos[1]].can_castle:
                if chessboard[1][pos[1]] == 0 and chessboard[2][pos[1]] == 0 and chessboard[3][pos[1]] == 0:
                    
                    possible_moves.append((2,pos[1]))

            if chessboard[7][pos[1]] != 0 and chessboard[7][pos[1]].can_castle:
                if chessboard[5][pos[1]] == 0  and chessboard[6][pos[1]] == 0:
                    
                    possible_moves.append((6,pos[1]))

        return possible_moves

    

    def render(self, screen, pos):
        sprite_rect = self.sprite.get_rect(center=pos)
        screen.blit(self.sprite, sprite_rect)

