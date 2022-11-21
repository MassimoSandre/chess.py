import pygame

class MaterialDisplayer():
    def __init__(self, box_size, sprites_size, padding, box_color, border_radius, spacings) -> None:
        self.__box_size = box_size
        self.__sprites_size = sprites_size
        self.__padding = padding
        self.__box_color = box_color
        self.__border_radius = border_radius
        self.__spacings = spacings
        self.__captured_material = []
        self.__values = {'q':9, 'r':5, 'b':3, 'n':3, 'p':1}

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

    def get_height(self):
        return self.__box_size[1]

    def get_width(self):
        return self.__box_size[0]

    def render(self, screen, position, font, sprites, material_advantage):
        pygame.draw.rect(screen, self.__box_color, (position, self.__box_size), 0, self.__border_radius)
        
        x = position[0] + self.__padding
        y = position[1] + self.__box_size[1]//2 - self.__sprites_size//2

        for i in range(len(self.__captured_material)):
            sprite = pygame.transform.scale(sprites[self.__captured_material[i]],(self.__sprites_size,self.__sprites_size))    
            if i != 0:
                if self.__captured_material[i] != self.__captured_material[i-1]:
                    x+=self.__spacings[1]
                else:
                    x+=self.__spacings[0]

            screen.blit(sprite, (x,y))
            x+=self.__sprites_size

        if material_advantage > 0:
            texts = font.render('+'+str(material_advantage), True, (255,255,255))
            y = position[1] - texts.get_rect().height//2 + self.__box_size[1]//2
            screen.blit(texts, (x,y))
