import pygame
import math
from GUI.GUIitem import GUIItem

class Timer(GUIItem):
    def __init__(self,time_in_seconds, increment, box_size, symbol_radius, padding, box_color, border_radius) -> None:
        super().__init__(box_size=box_size, padding=padding, box_color=box_color, border_radius=border_radius)
        self.__initial_time = time_in_seconds
        self.__time = time_in_seconds
        self.__increment = increment
        self.__symbol_radius = symbol_radius

    def reset(self):
        super().reset()
        self.__time = self.__initial_time

    def update(self, time_lapsed):
        self.__time -= time_lapsed
        if self.__time < 0:
            self.__time = 0
            return False
        return True

    def set_time(self, time):
        self.__time = time

    def make_move(self):
        self.__time += self.__increment

    def render(self, screen, position, font):
        super().render(screen=screen, position=position)
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

        screen.blit(s, (position[0] + self.padding , position[1] + self.padding//2))

        minutes = str(int(self.__time//60))
        seconds = self.__time%60

        time_string = ''
        if minutes == '0':
            if seconds < 20:
                time_string = str(int(seconds*10)/10)
            else:
                time_string = str(int(seconds))
        elif seconds < 10:
            time_string = minutes + ':0' + str(int(seconds))
        else:
            time_string = minutes + ':' + str(int(seconds))
        
        texts = font.render(time_string, True, (255,255,255))

        offset_x = texts.get_rect().width//2
        offset_y = texts.get_rect().height//2

        text_x = position[0] + (self.box_size[0] - (self.padding*2 + self.__symbol_radius*2))//2 - offset_x + (self.padding*2 + self.__symbol_radius*2)
        text_y = position[1] + self.box_size[1]//2 - offset_y

        screen.blit(texts, (text_x,text_y))
        
