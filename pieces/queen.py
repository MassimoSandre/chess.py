import pygame
from pieces.piece import Piece

class Queen(Piece):
    def __init__(self, is_white):
        if is_white:
            self.sprite = pygame.image.load('images/whitequeen.png').convert_alpha()
        else:
            self.sprite = pygame.image.load('images/blackqueen.png').convert_alpha()
        Piece.__init__(self=self,is_white=is_white)

    def get_possibile_moves(self, chessboard, pos):
        possibile_moves = []

        i = pos[0]-1
        j = pos[1]-1

        while i >= 0 and j >= 0:
            if chessboard[i][j] == 0:
                possibile_moves.append((i,j))
            else:
                if self.is_white ^ chessboard[i][j].is_white:
                    possibile_moves.append((i,j))
                break
            i = i - 1
            j = j - 1

        i = pos[0]+1
        j = pos[1]-1

        while i < len(chessboard) and j >= 0:
            if chessboard[i][j] == 0:
                possibile_moves.append((i,j))
            else:
                if self.is_white ^ chessboard[i][j].is_white:
                    possibile_moves.append((i,j))
                break
            i = i + 1
            j = j - 1
        
        i = pos[0]+1
        j = pos[1]+1

        while i < len(chessboard) and j < len(chessboard[i]):
            if chessboard[i][j] == 0:
                possibile_moves.append((i,j))
            else:
                if self.is_white ^ chessboard[i][j].is_white:
                    possibile_moves.append((i,j))
                break
            i = i + 1
            j = j + 1

        i = pos[0]-1
        j = pos[1]+1

        while i >= 0 and j < len(chessboard[i]):
            if chessboard[i][j] == 0:
                possibile_moves.append((i,j))
            else:
                if self.is_white ^ chessboard[i][j].is_white:
                    possibile_moves.append((i,j))
                break
            i = i - 1
            j = j + 1
        
        for i in range(pos[1]-1, -1, -1):
            if chessboard[pos[0]][i] == 0:
                possibile_moves.append((pos[0], i))
            else:
                if self.is_white ^ chessboard[pos[0]][i].is_white:
                    possibile_moves.append((pos[0], i))
                break

        for i in range(pos[1]+1, len(chessboard[pos[1]])):
            if chessboard[pos[0]][i] == 0:
                possibile_moves.append((pos[0], i))
            else:
                if self.is_white ^ chessboard[pos[0]][i].is_white:
                    possibile_moves.append((pos[0], i))
                break

        for i in range(pos[0]+1, len(chessboard)):
            if chessboard[i][pos[1]] == 0:
                possibile_moves.append((i, pos[1]))
            else:
                if self.is_white ^ chessboard[i][pos[1]].is_white:
                    possibile_moves.append((i, pos[1]))
                break

        for i in range(pos[0]-1, -1, -1):
            if chessboard[i][pos[1]] == 0:
                possibile_moves.append((i, pos[1]))
            else:
                if self.is_white ^ chessboard[i][pos[1]].is_white:
                    possibile_moves.append((i, pos[1]))
                break

        return possibile_moves

    def render(self, screen, pos):
        sprite_rect = self.sprite.get_rect(center=pos)
        screen.blit(self.sprite, sprite_rect)

