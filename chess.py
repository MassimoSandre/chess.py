import pygame
from chessboard import Chessboard
import default_game
from pieces.king import King
from pieces.pawn import Pawn
from pieces.queen import Queen
from pieces.rook import Rook
from pieces.knight import Knight
from pieces.bishop import Bishop
from GUI.timer import Timer
from GUI.material_displayer import MaterialDisplayer
from GUI.scoreboard import Scoreboard

class ChessGame:
    def __init__(self,*,grid_size=(8,8), cell_size=75, board_padding=10, board_colors=[(75, 81, 152),(151, 147, 204)], chessboard_size, margin=10, player_1, player_2,board_flipping=True, default_view_as_player_1=True) -> None:
        self.__pieces_classes = {'k':King, 'n':Knight, 'q':Queen, 'b':Bishop, 'r':Rook, 'p':Pawn}

        self.__margin = margin

        self.__board_flipping = board_flipping
        self.__default_view_as_player_1 = not default_view_as_player_1

        self.__white_player = player_2
        self.__black_player = player_1

        self.__grid_size = grid_size

        self.__board = Chessboard(chessboard_size, grid_size, cell_size, board_padding)

        self.__board.set_colors(*board_colors)
        self.__load_sprites()
        self.set_timer_settings()
        self.set_material_displayer_settings()
        self.set_scoreboard_settings()
        
        self.reset_game()

    def set_timer_settings(self,*,timer_time_in_seconds=300, timer_increment=0, timer_box_size=(150,50), timer_symbol_radius=20, timer_padding=10, timer_box_color=(100,100,100), timer_border_radius=4):
        self.__white_timer = Timer(timer_time_in_seconds, timer_increment, timer_box_size, timer_symbol_radius, timer_padding, timer_box_color, timer_border_radius)
        self.__black_timer = Timer(timer_time_in_seconds, timer_increment, timer_box_size, timer_symbol_radius, timer_padding, timer_box_color, timer_border_radius)

    def set_material_displayer_settings(self, displayer_box_size=(200,50), displayer_sprites_size=20,displayer_padding=10, displayer_box_color=(100,100,100), displayer_border_radius=4, spacings=(-15,0)):
        self.__white_material_displayer = MaterialDisplayer(displayer_box_size, displayer_sprites_size, displayer_padding, displayer_box_color, displayer_border_radius, spacings)
        self.__black_material_displayer = MaterialDisplayer(displayer_box_size, displayer_sprites_size, displayer_padding, displayer_box_color, displayer_border_radius, spacings)

    def set_scoreboard_settings(self, scoreboard_initial_values=(0,0,0), scoreboard_box_size=(40, 150), scoreboard_padding=10, scoreboard_box_color=(100,100,100), scoreboard_border_radius=4):
        self.__scoreboard = Scoreboard(scoreboard_initial_values, scoreboard_box_size, scoreboard_padding, scoreboard_box_color, scoreboard_border_radius)

    def __load_sprites(self):
        self.__sprites = {}
        self.__sprites['k'] = pygame.image.load('images/blackking.png').convert_alpha()
        self.__sprites['q'] = pygame.image.load('images/blackqueen.png').convert_alpha()
        self.__sprites['r'] = pygame.image.load('images/blackrook.png').convert_alpha()
        self.__sprites['b'] = pygame.image.load('images/blackbishop.png').convert_alpha()
        self.__sprites['n'] = pygame.image.load('images/blackknight.png').convert_alpha()
        self.__sprites['p'] = pygame.image.load('images/blackpawn.png').convert_alpha()
        self.__sprites['K'] = pygame.image.load('images/whiteking.png').convert_alpha()
        self.__sprites['Q'] = pygame.image.load('images/whitequeen.png').convert_alpha()
        self.__sprites['R'] = pygame.image.load('images/whiterook.png').convert_alpha()
        self.__sprites['B'] = pygame.image.load('images/whitebishop.png').convert_alpha()
        self.__sprites['N'] = pygame.image.load('images/whiteknight.png').convert_alpha()
        self.__sprites['P'] = pygame.image.load('images/whitepawn.png').convert_alpha()


    def set_colors(self, boards_colors):
        self.__board.set_colors(*boards_colors)

    def set_chessboard_position(self, chessboard_position):
        self.__board.set_pos(chessboard_position)

    def set_chessboard_cell_size(self, cell_size):
        self.__board.set_cell_size(cell_size)

    def get_current_turn(self):
        return self.__is_white_turn

    def __variables_reset(self):
        self.__view_as_white = True
        self.__is_white_turn = True
        self.__turn_switching = False

        self.__game_started = False

        self.__starting_cell = (0,0)

        self.__promoting = False
        self.__promoting_cell = None

        self.__clicked_piece = None

        self.__dragging = False

        self.__last_move = []

        self.__drawing = False
        self.__selected_cells = []
        self.__arrows = []

        self.__white_material_advantage = 0

        self.__moves = []
        self.__current_move = 1
        self.__semimoves = 0

        self.result = None

        self.__white_player, self.__black_player = self.__black_player, self.__white_player
        self.__white_player.set_color(True)
        self.__black_player.set_color(False)

        self.__scoreboard.flip_scores()

        self.__default_view_as_player_1 = not self.__default_view_as_player_1
        
        if not self.__board_flipping:
            self.__view_as_white = self.__default_view_as_player_1


    def reset_game(self):
        self.__variables_reset()
        self.__white_timer.reset()
        self.__black_timer.reset()
        self.__white_material_displayer.reset()
        self.__black_material_displayer.reset()
        self.load_position_from_fen_string(default_game.default_game_string)

    def load_position_from_fen_string(self, fen_string):
        fields = fen_string.split(' ')
        ranks = fields[0].split('/')
        ranks.reverse()
        for a in enumerate(ranks):
            row, rank = a
            col = 0
            for c in rank:
                if c.isdigit():
                    for k in range(col,col+int(c)):
                        self.__board.pieces[k][row] = 0
                    col += int(c)

                else:
                    d = self.__pieces_classes
                    self.__board.pieces[col][row] = d[c.lower()](c.isupper(), self.__sprites[c])
                    col += 1
        
        
        self.__is_white_turn = fields[1] == 'w'
        if self.__board_flipping:
            self.__view_as_white = self.__is_white_turn

        for castling in fields[2]:
            match castling:
                case 'K':
                    self.__board.pieces[4][0].can_castle = True
                    self.__board.pieces[7][0].can_castle = True
                case 'k':
                    self.__board.pieces[4][7].can_castle = True
                    self.__board.pieces[7][7].can_castle = True
                case 'Q':
                    self.__board.pieces[0][0].can_castle = True
                    self.__board.pieces[4][0].can_castle = True
                case 'q':
                    self.__board.pieces[4][7].can_castle = True
                    self.__board.pieces[0][7].can_castle = True

        if fields[3] != '-':
            row = int(fields[3][1])
            col = ord(fields[3][0])-97
            if row == 3:
                row = 2
            if row == 6:
                row = 7
            self.__board.pieces[col][row].can_be_captured_en_passant = True

        self.__semimoves = int(fields[4])
        
        self.__current_move = int(fields[5])
        self.__moves.append(fields[5] + '.')

        if self.__semimoves%2 == 1:
            self.__moves[0] += '..'


    def left_click_pressed(self, event):
        self.__arrows = []
        self.__selected_cells = []
        if self.__promoting:
            # check which new piece the user has selected
            clicked_cell = self.__board.get_cell_by_position(event.pos, True, False)
            
            if self.__is_white_turn ^ self.__view_as_white:
                if self.__is_white_turn:
                    x = (clicked_cell[0]-(self.__grid_size[0]-self.__promoting_cell-1), clicked_cell[1])
                else:
                    x = (clicked_cell[0] - self.__promoting_cell, clicked_cell[1])
            else:
                if self.__is_white_turn:
                    x = (clicked_cell[0]-self.__promoting_cell, clicked_cell[1]-(self.__grid_size[1]-2))
                else:
                    x = (clicked_cell[0]-(self.__grid_size[0]-self.__promoting_cell-1), clicked_cell[1]-(self.__grid_size[1]-2))
            

            #self.__promoting = False
            if x == (0,1):
                if self.__is_white_turn:
                    self.__white_player.set_promoting_choice('Q')
                else:
                    self.__black_player.set_promoting_choice('q')
                #self.__board.add_piece(cell_to_update, Queen(self.__board.pieces[cell_to_update[0]][cell_to_update[1]].is_white, self.__sprites['Q'] if self.__board.pieces[cell_to_update[0]][cell_to_update[1]].is_white else self.__sprites['q']))
            elif x == (1,1):
                if self.__is_white_turn:
                    self.__white_player.set_promoting_choice('R')
                else:
                    self.__black_player.set_promoting_choice('r')
                #self.__board.add_piece(cell_to_update, Rook(self.__board.pieces[cell_to_update[0]][cell_to_update[1]].is_white, self.__sprites['R'] if self.__board.pieces[cell_to_update[0]][cell_to_update[1]].is_white else self.__sprites['r']))
            elif x == (0,0):
                if self.__is_white_turn:
                    self.__white_player.set_promoting_choice('B')
                else:
                    self.__black_player.set_promoting_choice('b')
                #self.__board.add_piece(cell_to_update, Bishop(self.__board.pieces[cell_to_update[0]][cell_to_update[1]].is_white, self.__sprites['B'] if self.__board.pieces[cell_to_update[0]][cell_to_update[1]].is_white else self.__sprites['b']))
            elif x == (1,0):
                if self.__is_white_turn:
                    self.__white_player.set_promoting_choice('N')
                else:
                    self.__black_player.set_promoting_choice('n')
                #self.__board.add_piece(cell_to_update, Knight(self.__board.pieces[cell_to_update[0]][cell_to_update[1]].is_white, self.__sprites['N'] if self.__board.pieces[cell_to_update[0]][cell_to_update[1]].is_white else self.__sprites['n']))
            #else:
            #    self.__promoting = True
        else:
            clicked_cell = self.__board.get_cell_by_position(event.pos, self.__view_as_white)
            if self.__clicked_piece != None and clicked_cell != None and clicked_cell in self.__board.get_piece_possible_moves(self.__clicked_piece):
                #self.__make_move(self.__clicked_piece, clicked_cell)
                if self.__is_white_turn:
                    self.__white_player.set_next_move(self.__clicked_piece, clicked_cell)
                else:
                    self.__black_player.set_next_move(self.__clicked_piece, clicked_cell)
            else: 

                clicked_cell = self.__board.get_cell_by_position(event.pos, self.__view_as_white)

                if clicked_cell != None:
                    x = self.__board.get_piece(clicked_cell)
                    if x != None:
                        if not(x.is_white ^ self.__is_white_turn):
                            self.__dragging = True
                            self.__starting_cell = clicked_cell

        self.__clicked_piece = None

    
    def right_click_pressed(self, event):
        self.__clicked_piece = None
        clicked_cell = self.__board.get_cell_by_position(event.pos, self.__view_as_white)
        if clicked_cell != None:
            self.__drawing = True
            self.__starting_cell = clicked_cell

    def middle_click_pressed(self, event):
        self.__view_as_white = not self.__view_as_white
    
    def left_click_released(self, event):
        if(self.__dragging):
            self.__dragging = False
            release_cell = self.__board.get_cell_by_position(event.pos, self.__view_as_white)
            if release_cell in self.__board.get_piece_possible_moves(self.__starting_cell):
                if self.__is_white_turn:
                    self.__white_player.set_next_move(self.__starting_cell, release_cell)
                    #self.__make_move(self.__starting_cell, release_cell)
                else:
                    self.__black_player.set_next_move(self.__starting_cell, release_cell)
                
            elif release_cell == self.__starting_cell:
                self.__clicked_piece = release_cell


    def right_click_released(self, event):
        if (self.__drawing):
            self.__drawing = False
            clicked_cell = self.__board.get_cell_by_position(event.pos, self.__view_as_white)
            if clicked_cell != None:
                if clicked_cell != self.__starting_cell:
                    if (self.__starting_cell[0], self.__starting_cell[1], clicked_cell[0], clicked_cell[1]) in self.__arrows:
                        self.__arrows.remove((self.__starting_cell[0], self.__starting_cell[1], clicked_cell[0], clicked_cell[1]))
                    else:
                        self.__arrows.append((self.__starting_cell[0], self.__starting_cell[1], clicked_cell[0], clicked_cell[1]))
                else:
                    if clicked_cell in self.__selected_cells:
                        self.__selected_cells.remove(clicked_cell)
                    else:
                        self.__selected_cells.append(clicked_cell)

    def __make_move(self, starting_cell, destination_cell):
        move = self.__board.get_move_code(starting_cell, destination_cell)
        self.__board.move_piece(starting_cell, destination_cell, definitive=True, castling_check=True, en_passant=True)

        if self.__board.check_for_checkmate(not self.__is_white_turn):
            move+='#'            
        elif self.__board.check_for_check(not self.__is_white_turn):
            move+='+'

        self.__turn_switching = True
        self.__last_move = [starting_cell, destination_cell]
        if self.__is_white_turn:
            self.__moves.append(str(self.__current_move) + '. ' + move + ' ')
        else:
            self.__moves[-1] += move
            self.__current_move+=1
            #print(self.__moves[-1])
        
        self.__semimoves+=1
            


    def update(self, time_lapsed):
        game = True

        x = self.__board.check_for_promotion()
        if x != None:
            self.__promoting = True
            self.__promoting_cell = x

        if self.__promoting:
            if self.__is_white_turn:
                r = 7
                p = self.__white_player.get_promoting_choice()
            else:
                r = 0
                p = self.__black_player.get_promoting_choice()

            if p != None:
                self.__promoting = False

                self.__board.add_piece((self.__promoting_cell,r), self.__pieces_classes[p.lower()](self.__board.pieces[self.__promoting_cell][r].is_white, self.__sprites[p]), p)


        if not self.__promoting and self.__turn_switching:
            if not self.__game_started:
                self.__game_started = True
            if self.__board.check_for_checkmate(not self.__is_white_turn):
                game = False
                if self.__is_white_turn:
                    self.result = (1,0)
                    self.__scoreboard.add_score((1,0,0))
                else:
                    self.result = (0,1)
                    self.__scoreboard.add_score((0,0,1))
            elif self.__board.check_for_stalemate(not self.__is_white_turn):
                game = False
                self.result = (0.5,0.5)
                self.__scoreboard.add_score((0,1,0))
            elif self.__board.check_for_insufficient_mating_material():
                game = False
                self.result = (0.5,0.5)
                self.__scoreboard.add_score((0,1,0))

            if self.__is_white_turn:
                self.__white_timer.make_move()
            else:
                self.__black_timer.make_move()
            self.__is_white_turn = not self.__is_white_turn
            if self.__board_flipping:
                self.__view_as_white = self.__is_white_turn
            self.__turn_switching = False

        self.__white_material_advantage = self.__white_material_displayer.get_total_material_value()-self.__black_material_displayer.get_total_material_value()

        capture = self.__board.get_capture()
        if capture != None:
            if capture.islower():
                self.__white_material_displayer.add_material(capture)
            else:
                self.__black_material_displayer.add_material(capture)
                
        timeout = False

        if self.__game_started:        
            if self.__is_white_turn:
                timeout = not self.__white_timer.update(time_lapsed)
            else:
                timeout = not self.__black_timer.update(time_lapsed)

        if game and timeout:
            self.winner = not self.__is_white_turn
            game = False

        if game:
            if self.__is_white_turn:
                m = self.__white_player.get_next_move(self.__board)
            else:
                m = self.__black_player.get_next_move(self.__board)
            if m != None:
                self.__make_move(*m)


        return game

    def render(self, screen, mouse_position, timer_font, displayer_font):
        self.__board.render(screen, self.__view_as_white)

        self.__board.render_highlighted_cells(screen, self.__view_as_white, self.__last_move, (40, 255, 40))
        self.__board.render_highlighted_cells(screen, self.__view_as_white, self.__selected_cells, (200, 30, 40))
        
        if self.__dragging:
            pr = self.__board.get_piece_possible_moves(self.__starting_cell)

            self.__board.render_possible_moves_cells(screen, self.__view_as_white, pr)

            self.__board.render_pieces(screen, self.__view_as_white,[self.__starting_cell])
            self.__board.render_dragging_piece(screen, self.__starting_cell, mouse_position)
        elif self.__clicked_piece != None:
            pr = self.__board.get_piece_possible_moves(self.__clicked_piece)

            self.__board.render_possible_moves_cells(screen, self.__view_as_white, pr)

            self.__board.render_pieces(screen, self.__view_as_white)
        else:
            self.__board.render_pieces(screen, self.__view_as_white)

        self.__board.render_arrows(screen, self.__view_as_white, self.__arrows, (255,150,60))

        if self.__promoting:
            self.__board.render_promoting_ui(screen, self.__is_white_turn,self.__view_as_white, self.__promoting_cell)

        top_timer_pos = list(self.__board.get_rect().topright)
        top_timer_pos[0]-=self.__white_timer.get_width()
        top_timer_pos[1]-=self.__white_timer.get_height()+self.__margin

        bottom_timer_pos = list(self.__board.get_rect().bottomright)
        bottom_timer_pos[0]-=self.__white_timer.get_width()
        bottom_timer_pos[1]+=self.__margin

        top_material_displayer_pos = list(self.__board.get_rect().topleft)
        top_material_displayer_pos[1]-=self.__white_material_displayer.get_height()+self.__margin

        bottom_material_displayer_pos = list(self.__board.get_rect().bottomleft)
        bottom_material_displayer_pos[1]+=self.__margin

        scoreboard_pos = list(self.__board.get_rect().topright)
        scoreboard_pos[0]+=self.__margin
        scoreboard_pos[1]+=self.__board.get_rect().height//2 - self.__scoreboard.get_height()//2

        if self.__view_as_white:
            self.__white_timer.render(screen, bottom_timer_pos, timer_font)
            self.__black_timer.render(screen, top_timer_pos, timer_font)

            self.__white_material_displayer.render(screen, bottom_material_displayer_pos, displayer_font, self.__sprites, self.__white_material_advantage)
            self.__black_material_displayer.render(screen, top_material_displayer_pos, displayer_font, self.__sprites, -self.__white_material_advantage)
        else:
            self.__white_timer.render(screen, top_timer_pos, timer_font)
            self.__black_timer.render(screen, bottom_timer_pos, timer_font)

            self.__white_material_displayer.render(screen, top_material_displayer_pos, displayer_font, self.__sprites, self.__white_material_advantage)
            self.__black_material_displayer.render(screen, bottom_material_displayer_pos, displayer_font, self.__sprites, -self.__white_material_advantage)

        self.__scoreboard.render(screen, scoreboard_pos, self.__view_as_white, timer_font)