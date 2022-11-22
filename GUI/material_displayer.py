import pygame
from GUI.GUIitem import GUIItem

class MaterialDisplayer(GUIItem):
    def __init__(self, box_size, sprites_size, padding, box_color, border_radius, spacings) -> None:
        super().__init__(box_size=box_size, padding=padding, box_color=box_color, border_radius=border_radius)
        self.__sprites_size = sprites_size
        self.__spacings = spacings
        self.__captured_material = []
        self.__values = {'q':9, 'r':5, 'b':3, 'n':3, 'p':1}

    def reset(self):
        super().reset()
        self.__captured_material = []

    def __sort_material(self):
        def f(e):
            return self.__values[e.lower()]
            
        self.__captured_material.sort(key=f)

    def add_material(self, material_code):
        self.__captured_material.append(material_code)
        self.__sort_material()

    def get_total_material_value(self):
        s = 0
        for m in self.__captured_material:
            s+=self.__values[m.lower()]
        return s

    def render(self, screen, position, font, sprites, material_advantage):
        super().render(screen=screen,position=position)
        
        x = position[0] + self.padding
        y = position[1] + self.box_size[1]//2 - self.__sprites_size//2

        for i in range(len(self.__captured_material)):
            sprite = pygame.transform.scale(sprites[self.__captured_material[i]],(self.__sprites_size,self.__sprites_size))
            mask = pygame.mask.from_surface(sprite) 
            
            if i != 0:
                if self.__captured_material[i] != self.__captured_material[i-1]:
                    x+=self.__spacings[1]
                else:
                    x+=self.__spacings[0]

            screen.blit(sprite, (x,y))
            outline = [(p[0] + x, p[1] + y) for p in mask.outline()]
            x+=self.__sprites_size
            if self.__captured_material[i].isupper():
                pygame.draw.lines(screen, (0,0,0), False, outline, 1)
            else:
                pygame.draw.lines(screen, (255,255,255), False, outline, 1)

        if material_advantage > 0:
            texts = font.render('+'+str(material_advantage), True, (255,255,255))
            y = position[1] - texts.get_rect().height//2 + self.box_size[1]//2
            screen.blit(texts, (x,y))
