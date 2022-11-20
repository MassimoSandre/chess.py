import pygame, sys
from pygame.locals import *
from chess import ChessGame
import default_game as default

# TODO
# HIGH PRIORITY
# - Menù
# - Algebraic notation
# - sounds
# - AI (stockfish 15)
# - sort of evaluation
# - timer and time control
# - collapse the online chess.py repository in here
#
# LOW PRIORITY
# - themes

# NOTE
# Remember ReiettoAyanami to do this in Rust

def main():
    # --- SETTINGS ---
    board_padding = 10
    grid_size = default.grid_size
    size = width, height = 800, 800

    colors = {'white': (255,255,255), 'black': (0,0,0), 'blue': (0,0,255), 'red': (255,0,0)}
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    pygame.display.set_caption('Sandretti\'s chess')
    pygame.font.init()
    clock = pygame.time.Clock()

    game = ChessGame(chessboard_size=(height//2,height//2), board_padding=board_padding)

    running = True
    game_ended = False
    mainfont = pygame.font.SysFont('Arial', 50)
    
    while running:
        if game_ended:
            game_ended = False
            game.reset_game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    game.left_click_pressed(event)
                elif event.button == 2:
                    game.middle_click_pressed(event)
                
                elif event.button == 3:
                    game.right_click_pressed(event)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    game.left_click_released(event)

                elif event.button == 3:
                    game.right_click_released(event)
                

        # --- UPDATE ---
        game_ended = not game.update()
        size = width,height = pygame.display.get_surface().get_size()
        game.set_chessboard_position((width//2, height//2))
        
        short_side = min(width, height-150)
        if short_side == width:
            cell_size = (short_side - (2*board_padding))//grid_size[0]
        else:
            cell_size = (short_side - (2*board_padding))//grid_size[1]
        cell_size = min(max(cell_size,75), 100)
        game.set_chessboard_cell_size(cell_size)

        # --- RENDER ---
        screen.fill(colors['black'])
        game.render(screen,pygame.mouse.get_pos())

        if game.get_current_turn():
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

if __name__ == "__main__":
    main()