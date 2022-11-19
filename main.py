import pygame, sys
from pygame.locals import *
from chessboard import Chessboard
from pieces.piece import Piece
from pieces.king import King
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.queen import Queen
import default_game as default


size = width, height = 800, 720

colors = {'white': (255,255,255), 'black': (0,0,0), 'blue': (0,0,255), 'red': (255,0,0)}

grid_size = (8,8)
board = Chessboard((int((width-600))/2,int((height-600)/2)+0), grid_size, (75,75))
board.set_colors((75, 81, 152), (151, 147, 204))

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Sandretti\'s chess')
pygame.font.init()

default.reset_board_to_default_game(board)

view_as_white = True        

clock = pygame.time.Clock()

running = True

white_check = False
black_check = False

is_white_turn = True
turn_switching = False

promoting = False
promoting_cell = 0

dragging = False
starting = 0

moved_piece = (0,0)

last_move = []

mainfont = pygame.font.SysFont('Comic Sans MS', 50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                if promoting:
                    # check which new piece the user has selected
                    clicked_cell = board.get_cell_by_position(event.pos, False)

                    if is_white_turn:
                        cell_to_update = (7-promoting_cell,7)
                    else:
                        cell_to_update = (promoting_cell,0)
                    
                    if is_white_turn ^ view_as_white:
                        x = (clicked_cell[0]-(grid_size[0]-promoting_cell-1), clicked_cell[1]-(grid_size[1]-2))
                    else:
                        x = (clicked_cell[0]-promoting_cell, clicked_cell[1])
                    

                    promoting = False
                    if x == (0,0):
                        board.add_piece(cell_to_update, Queen(board.pieces[cell_to_update[0]][cell_to_update[1]].is_white))
                        pass
                    elif x == (1,0):
                        board.add_piece(cell_to_update, Rook(board.pieces[cell_to_update[0]][cell_to_update[1]].is_white))
                        pass
                    elif x == (0,1):
                        board.add_piece(cell_to_update, Bishop(board.pieces[cell_to_update[0]][cell_to_update[1]].is_white))
                        pass
                    elif x == (1,1):
                        board.add_piece(cell_to_update, Knight(board.pieces[cell_to_update[0]][cell_to_update[1]].is_white))
                        pass
                    else:
                        promoting = True
                else:
                    clicked_cell = board.get_cell_by_position(event.pos, view_as_white)

                    if clicked_cell != None:
                        x = board.get_piece(clicked_cell)
                        if x != None:
                            
                            if not(x.is_white ^ is_white_turn):
                                dragging = True
                                starting_cell = clicked_cell
            elif event.button == 2:
                view_as_white = not view_as_white
        
        if event.type == pygame.MOUSEBUTTONUP:
            if(dragging):
                #print(starting_cell)
                dragging = False
                release_cell = board.get_cell_by_position(event.pos, view_as_white)
                if release_cell in board.get_piece_possibile_moves(starting_cell):
                    board.move_piece(starting_cell, release_cell)
                    turn_switching = True
                    moved_piece = release_cell
                    last_move = [starting_cell, release_cell]
            

    # --- UPDATE ---
    x = board.check_for_promotion(is_white_turn)
    
    if x != None:
        promoting = True
        promoting_cell = x

    if not promoting and turn_switching:
        if board.check_for_checkmate(not view_as_white):
            print("CHECKMATE")
            running = False
        is_white_turn = not is_white_turn
        view_as_white = is_white_turn
        turn_switching = False

    # --- RENDER ---
    screen.fill(colors['black'])
    board.render(screen, view_as_white)

    board.render_highlighted_cells(screen, view_as_white, last_move,(40,255,40))

    if dragging:
        pr = board.get_piece_possibile_moves(starting_cell)

        board.render_possibile_moves_cells(screen, view_as_white, pr)
        
        board.render_pieces(screen, view_as_white,[starting_cell])
        board.render_dragging_piece(screen, starting_cell, pygame.mouse.get_pos())
    else:
        board.render_pieces(screen, view_as_white)

    if promoting:
        board.render_promoting_ui(screen, is_white_turn,view_as_white, promoting_cell)

    if view_as_white ^ is_white_turn:
        texts = mainfont.render("It's your opponent's turn", False, (255,255,255))
    else:
        texts = mainfont.render("It's your turn", False, (255,255,255))  
    offset_x = int(texts.get_rect().width/2)
    

    pygame.display.update()
    clock.tick(60)


pygame.quit()
sys.exit()