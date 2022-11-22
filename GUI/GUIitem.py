import pygame

class GUIItem:
    def __init__(self, box_size, padding, box_color, border_radius) -> None:
        self.box_size = list(box_size)
        self.padding = padding
        self.box_color = box_color
        self.border_radius = border_radius

    def reset(self):
        pass

    def get_height(self):
        return self.box_size[1]

    def set_height(self, height):
        self.box_size[1] = height

    def get_width(self):
        return self.box_size[0]

    def set_width(self, width):
        self.box_size[0] = width

    def get_padding(self):
        return self.padding

    def set_padding(self, padding):
        self.padding = padding

    def get_box_color(self):
        return self.box_color

    def set_box_color(self, box_color):
        self.box_color = box_color

    def get_border_radius(self):
        return self.border_radius

    def set_border_radius(self, border_radius):
        self.border_radius = border_radius

    def render(self, screen, position):
        pygame.draw.rect(screen, self.box_color, (position, self.box_size), 0, self.border_radius)