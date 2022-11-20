from chessboard import Chessboard
import default_game
from pieces.queen import Queen
from pieces.rook import Rook
from pieces.knight import Knight
from pieces.bishop import Bishop

class ChessGame:
    def __init__(self,*,grid_size=(8,8), cell_size=75, board_padding=10, board_colors=[(75, 81, 152),(151, 147, 204)], chessboard_size) -> None:
        self.__board = Chessboard(chessboard_size, grid_size, cell_size, board_padding)
        self.__board.set_colors(*board_colors)
        self.reset_game()
        self.__view_as_white = True
        self.__is_white_turn = True
        self.__turn_switching = False

        self.__starting_cell = (0,0)

        self.__promoting = False
        self.__promoting_cell = 0

        self.__dragging = False

        self.__last_move = []

        self.__drawing = False
        self.__selected_cells = []
        self.__arrows = []

        
    def reset_game(self):
        default_game.reset_board_to_default_game(self.__board)

    def left_click_pressed(self, event):
        self.__arrows = []
        self.__selected_cells = []
        if self.__promoting:
            # check which new piece the user has selected
            clicked_cell = self.__board.get_cell_by_position(event.pos, False, False)

            if self.__is_white_turn:
                cell_to_update = (7-self.__promoting_cell,7)
            else:
                cell_to_update = (self.__promoting_cell,0)
            
            if self.__is_white_turn ^ self.__view_as_white:
                x = (clicked_cell[0]-(self.__grid_size[0]-self.__promoting_cell-1), clicked_cell[1]-(self.__grid_size[1]-2))
            else:
                x = (clicked_cell[0]-self.__promoting_cell, clicked_cell[1])
            

            self.__promoting = False
            if x == (0,0):
                self.__board.add_piece(cell_to_update, Queen(self.__board.pieces[cell_to_update[0]][cell_to_update[1]].is_white))
                pass
            elif x == (-1,0):
                self.__board.add_piece(cell_to_update, Rook(self.__board.pieces[cell_to_update[0]][cell_to_update[1]].is_white))
                pass
            elif x == (0,1):
                self.__board.add_piece(cell_to_update, Bishop(self.__board.pieces[cell_to_update[0]][cell_to_update[1]].is_white))
                pass
            elif x == (-1,1):
                self.__board.add_piece(cell_to_update, Knight(self.__board.pieces[cell_to_update[0]][cell_to_update[1]].is_white))
                pass
            else:
                self.__promoting = True
        else:
            clicked_cell = self.__board.get_cell_by_position(event.pos, self.__view_as_white)

            if clicked_cell != None:
                x = self.__board.get_piece(clicked_cell)
                if x != None:
                    if not(x.is_white ^ self.__is_white_turn):
                        self.__dragging = True
                        self.__starting_cell = clicked_cell
    
    def right_click_pressed(self, event):
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
                self.__board.move_piece(self.__starting_cell, release_cell, definitive=True, castling_check=True, en_passant=True)
                self.__turn_switching = True
                self.__last_move = [self.__starting_cell, release_cell]

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

    def update(self):
        game_ended = True
        x = self.__board.check_for_promotion(self.__is_white_turn)
        
        if x != None:
            self.__promoting = True
            self.__promoting_cell = x

        if not self.__promoting and self.__turn_switching:
            if self.__board.check_for_checkmate(not self.__view_as_white):
                game_ended = False
            self.__is_white_turn = not self.__is_white_turn
            self.__view_as_white = self.__is_white_turn
            self.__turn_switching = False

        return game_ended

    def render(self, screen, mouse_position):
        self.__board.render(screen, self.__view_as_white)

        self.__board.render_highlighted_cells(screen, self.__view_as_white, self.__last_move, (40, 255, 40))
        self.__board.render_highlighted_cells(screen, self.__view_as_white, self.__selected_cells, (200, 30, 40))
        
        if self.__dragging:
            pr = self.__board.get_piece_possible_moves(self.__starting_cell)

            self.__board.render_possible_moves_cells(screen, self.__view_as_white, pr)
            
            self.__board.render_pieces(screen, self.__view_as_white,[self.__starting_cell])
            self.__board.render_dragging_piece(screen, self.__starting_cell, mouse_position)
        else:
            self.__board.render_pieces(screen, self.__view_as_white)

        self.__board.render_arrows(screen, self.__view_as_white, self.__arrows, (255,127,80))

        if self.__promoting:
            self.__board.render_promoting_ui(screen, self.__is_white_turn,self.__view_as_white, self.__promoting_cell)

