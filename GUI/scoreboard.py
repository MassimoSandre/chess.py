from GUI.GUIitem import GUIItem 

class Scoreboard(GUIItem):
    def __init__(self, initial_values, box_size, padding, box_color, border_radius) -> None:
        super().__init__(box_size=box_size, padding=padding, box_color=box_color, border_radius=border_radius)
        
        self.__scores = list(initial_values)

    def reset(self):
        super().reset()
        self.__scores = (0,0,0)

    def add_score(self,score):
        self.__scores[0] += score[0]
        self.__scores[1] += score[1]
        self.__scores[2] += score[2]

    def flip_scores(self):
        self.__scores.reverse()

    def render(self, screen, position, view_as_white,font):
        super().render(screen=screen, position=position)
        
        top_score_text = font.render(str(self.__scores[0]), True, (255,255,255))
        draws_text = font.render(str(self.__scores[1]), True, (255,255,255))
        bottom_score_text = font.render(str(self.__scores[2]), True, (255,255,255))

        if view_as_white:
            top_score_text, bottom_score_text = bottom_score_text, top_score_text

        x_1 = position[0] + self.box_size[0]//2 - top_score_text.get_rect().width//2
        y_1 = position[1] + self.padding

        x_2 = position[0] + self.box_size[0]//2 - draws_text.get_rect().width//2
        y_2 = position[1] + self.box_size[1]//2 - draws_text.get_rect().height//2

        x_3 = position[0] + self.box_size[0]//2 - bottom_score_text.get_rect().width//2
        y_3 = position[1] + self.box_size[1] - self.padding - bottom_score_text.get_rect().height

        
        screen.blit(top_score_text, (x_1,y_1))
        screen.blit(draws_text, (x_2,y_2))
        screen.blit(bottom_score_text, (x_3,y_3))
        