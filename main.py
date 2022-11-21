import pygame, sys
from pygame.locals import *
from chess import ChessGame
import default_game as default


# TODO
# HIGH PRIORITY
# - menù
# - improve algebraic notation 
# - sounds
# - AI (stockfish 15)
# - sort of evaluation
# - collapse the online chess.py repository in here
# - captured material
#
# LOW PRIORITY
# - themes

# NOTE
# Remember ReiettoAyanami to do this in Rust


def main():
    # --- SETTINGS ---
    board_padding = 10
    grid_size = default.grid_size
    time_on_clock = default.default_starting_time
    timer_increment = default.default_increment

    size = width, height = 800, 800

    colors = {'white': (255,255,255), 'black': (0,0,0), 'blue': (0,0,255), 'red': (255,0,0)}
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    pygame.display.set_caption('Sandretti\'s chess')
    pygame.font.init()
    clock = pygame.time.Clock()

    game = ChessGame(chessboard_size=(height//2,height//2), board_padding=board_padding)
    game.set_timer_settings(timer_time_in_seconds=time_on_clock, timer_increment=timer_increment)

    running = True
    game_ended = False
    mainfont = pygame.font.SysFont('Arial', 35)
    displayer_font = pygame.font.SysFont('Arial', 18)
    ready = False
    last_update = 0 
    time_lapsed = 0

    while running:
        if game_ended:
            game_ended = False
            if game.result == (1,0):
                print("White wins")
            elif game.result == (0,1):
                print("Black wins")
            else:
                print("Draw")
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
        if ready:
            time_lapsed = (pygame.time.get_ticks() - last_update)/1000
            last_update = pygame.time.get_ticks()

        game_ended = not game.update(time_lapsed)
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
        game.render(screen,pygame.mouse.get_pos(), mainfont, displayer_font)

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

        if not ready:
            ready = True
            last_update = pygame.time.get_ticks()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()