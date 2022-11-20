import pygame, sys
from pygame.locals import *
from chessboard import Chessboard
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.queen import Queen
import default_game as default

# TODO
# HIGH PRIORITY
# - Menù
# - FEN implementation
# - Algebric notation
# - sounds
# - AI (stockfish 15)
# - sort of evaluation
# - timer and time control
# - collapse the online chess.py repository in here
# - arrows
#
# LOW PRIORITY
# - themes

# NOTE
# Remember ReiettoAyanami to do this in Rust

size = width, height = 800, 800

colors = {'white': (255,255,255), 'black': (0,0,0), 'blue': (0,0,255), 'red': (255,0,0)}

grid_size = (8,8)
cell_size = 75
board_padding = 10
board = Chessboard((height//2,height//2), grid_size, cell_size, board_padding)
board.set_colors((75, 81, 152), (151, 147, 204))

screen = pygame.display.set_mode(size, pygame.RESIZABLE)
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

starting_cell = (0,0)

promoting = False
promoting_cell = 0

dragging = False
starting = 0

moved_piece = (0,0)

last_move = []

drawing = False
selected_cells = []
arrows = []

mainfont = pygame.font.SysFont('Arial', 50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                arrows = []
                selected_cells = []
                if promoting:
                    # check which new piece the user has selected
                    clicked_cell = board.get_cell_by_position(event.pos, False, False)

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
                    elif x == (-1,0):
                        board.add_piece(cell_to_update, Rook(board.pieces[cell_to_update[0]][cell_to_update[1]].is_white))
                        pass
                    elif x == (0,1):
                        board.add_piece(cell_to_update, Bishop(board.pieces[cell_to_update[0]][cell_to_update[1]].is_white))
                        pass
                    elif x == (-1,1):
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
            
            elif event.button == 3:
                clicked_cell = board.get_cell_by_position(event.pos, view_as_white)
                if clicked_cell != None:
                    drawing = True
                    starting_cell = clicked_cell

        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if(dragging):
                    
                    dragging = False
                    release_cell = board.get_cell_by_position(event.pos, view_as_white)
                    if release_cell in board.get_piece_possible_moves(starting_cell):
                        board.move_piece(starting_cell, release_cell, definitive=True, castling_check=True, en_passant=True)
                        turn_switching = True
                        moved_piece = release_cell
                        last_move = [starting_cell, release_cell]

            elif event.button == 3:
                if (drawing):
                    drawing = False
                    clicked_cell = board.get_cell_by_position(event.pos, view_as_white)
                    if clicked_cell != None:
                        if clicked_cell != starting_cell:
                            if (starting_cell[0], starting_cell[1], clicked_cell[0], clicked_cell[1]) in arrows:
                                arrows.remove((starting_cell[0], starting_cell[1], clicked_cell[0], clicked_cell[1]))
                            else:
                                arrows.append((starting_cell[0], starting_cell[1], clicked_cell[0], clicked_cell[1]))
                        else:
                            if clicked_cell in selected_cells:
                                selected_cells.remove(clicked_cell)
                            else:
                                selected_cells.append(clicked_cell)
            

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

    size = width,height = pygame.display.get_surface().get_size()

    board.set_pos((width//2, height//2))

    short_side = min(width, height-150)

    if short_side == width:
        cell_size = (short_side - (2*board_padding))//grid_size[0]
    else:
        cell_size = (short_side - (2*board_padding))//grid_size[1]
    
    cell_size = min(max(cell_size,75), 100)

    board.set_cell_size(cell_size)

    # --- RENDER ---
    screen.fill(colors['black'])
    board.render(screen, view_as_white)

    board.render_highlighted_cells(screen, view_as_white, last_move, (40, 255, 40))
    board.render_highlighted_cells(screen, view_as_white, selected_cells, (200, 30, 40))
    
    if dragging:
        pr = board.get_piece_possible_moves(starting_cell)

        board.render_possible_moves_cells(screen, view_as_white, pr)
        
        board.render_pieces(screen, view_as_white,[starting_cell])
        board.render_dragging_piece(screen, starting_cell, pygame.mouse.get_pos())
    else:
        board.render_pieces(screen, view_as_white)

    board.render_arrows(screen, view_as_white, arrows, (255,127,80))

    if promoting:
        board.render_promoting_ui(screen, is_white_turn,view_as_white, promoting_cell)

    if is_white_turn:
        texts = mainfont.render("It's White's turn", True, (255,255,255))
    else:
        texts = mainfont.render("It's Black's turn", True, (255,255,255))  
    offset_x = texts.get_rect().width//2
    offset_y = texts.get_rect().height//2

    text_x = width//2 - offset_x
    text_y = (height - (grid_size[1]*cell_size))//4 - offset_y

    screen.blit(texts, (text_x,text_y))

    pygame.display.update()
    clock.tick(60)


pygame.quit()
sys.exit()