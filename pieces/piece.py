import pygame

class Piece():
    def __init__(self, is_white):
        self.is_white = is_white
        self.is_promotable = False
        self.is_king = False
        self.can_castle = False
        self.original_sprite_size = (self.sprite.get_rect().width, self.sprite.get_rect().height)
        self.can_be_captured_en_passant = False
        

    def move(self):
        pass

    def get_possible_moves(self, chessboard, pos):
        return []

    def scale_by(self, factor):
        self.sprite = pygame.transform.scale(self.sprite,(int(self.original_sprite_size[0]*factor),int(self.original_sprite_size[1]*factor)))

    def render(self, screen, pos):
        sprite_rect = self.sprite.get_rect(center=pos)
        screen.blit(self.sprite, sprite_rect)
