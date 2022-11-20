import pygame
import math

class Timer:
    def __init__(self,*,time_in_seconds=600, increment=0, box_size=(150,50), symbol_radius=20, padding=10, box_color=(100,100,100), border_radius=4) -> None:
        self.__initial_time = time_in_seconds
        self.__time = time_in_seconds
        self.__increment = increment
        self.__box_size = box_size
        self.__symbol_radius = symbol_radius
        self.__padding = padding
        self.__box_color = box_color
        self.__border_radius = border_radius

    def update(self, time_lapsed):
        self.__time -= time_lapsed

    def make_move(self):
        self.__time += self.__increment

    def reset(self):
        self.__time = self.__initial_time
    
    def get_height(self):
        return self.__box_size[1]

    def get_width(self):
        return self.__box_size[0]

    def render(self, screen, position, font):
        pygame.draw.rect(screen, self.__box_color, (position, self.__box_size), 0, self.__border_radius)
        s = pygame.Surface((self.__symbol_radius*2, self.__symbol_radius*2), pygame.SRCALPHA)
        s.fill((255,255,255,0))
        pygame.draw.circle(s, (255,255,255, 255), (self.__symbol_radius, self.__symbol_radius), self.__symbol_radius)

        if self.__time < self.__initial_time:
            points = [(self.__symbol_radius,self.__symbol_radius),(self.__symbol_radius,0), (0,0)]
            angle =2*math.pi - 2*(self.__time/self.__initial_time)*math.pi
            
            if angle > math.pi/2:
                points.append((0, self.__symbol_radius*2))
            if angle > math.pi:
                points.append((self.__symbol_radius*2, self.__symbol_radius*2))
            if angle > (math.pi/2)*3:
                points.append((self.__symbol_radius*2, 0))

            fixed_angle = angle + math.pi/2

            x = self.__symbol_radius*math.cos(fixed_angle) + self.__symbol_radius
            y = - self.__symbol_radius*math.sin(fixed_angle) + self.__symbol_radius

            points.append((x,y))
            
            pygame.draw.polygon(s, (0,0,0,0),points)

        screen.blit(s, (position[0] + self.__padding , position[1] + self.__padding//2))

        minutes = str(int(self.__time//60))
        seconds = str(int(self.__time%60))

        time_string = ''
        if minutes == '0':
            time_string = seconds
        elif len(seconds) != 2:
            time_string = minutes + ':0' + seconds
        else:
            time_string = minutes + ':' + seconds
        
        texts = font.render(time_string, True, (255,255,255))

        offset_x = texts.get_rect().width//2
        offset_y = texts.get_rect().height//2

        text_x = position[0] + (self.__box_size[0] - (self.__padding*2 + self.__symbol_radius*2))//2 - offset_x + (self.__padding*2 + self.__symbol_radius*2)
        text_y = position[1] + self.__box_size[1]//2 - offset_y

        screen.blit(texts, (text_x,text_y))
        
