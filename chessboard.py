import pygame
from pieces.piece import Piece
from pieces.king import King

class Chessboard():
    def __init__(self, pos, board_size , cell_size):
        self.pos_x, self.pos_y = pos
        self.board_width, self.board_height = board_size
        self.cell_width, self.cell_height = cell_size
        
        # i create the actual matrix:
        self.pieces = []
        for i in range(self.board_width):
            temp = []
            for j in range(self.board_height):
                temp.append(0)
            self.pieces.append(temp)

    
    def set_colors(self, color_1, color_2):
        self.color_1 = color_1
        self.color_2 = color_2

    def get_piece(self, cell):
        x,y = cell
        if self.pieces[x][y] == 0:
            return None
        return self.pieces[x][y]

    # returns a tuple which represents the coordinates of the cell the position falls
    def get_cell_by_position(self, pos, player_is_white):
        tx = pos[0] - self.pos_x
        ty  = pos[1] - self.pos_y
        
        x = int(tx/self.cell_width)
        y = int(ty/self.cell_height)

        if x < 0 or y < 0 or x >= self.board_width or y >= self.board_height:
            return None

        if player_is_white:
            return (7-x,7-y)
        else:
            return (x, y)

    def remove_piece(self, pos):
        self.add_piece(pos, 0)

    def add_piece(self, pos, piece):
        self.pieces[pos[0]][pos[1]] = piece

    def move_piece(self, starting_pos, destination_pos):
        self.add_piece(destination_pos, self.pieces[starting_pos[0]][starting_pos[1]])
        self.remove_piece(starting_pos)
        self.get_piece(destination_pos).move()
        
    def get_piece_possibile_moves_raw(self, pos):
        x = self.pieces[pos[0]][pos[1]].get_possibile_moves(self.pieces, (pos[0],pos[1]))
        
        return x

    def get_piece_possibile_moves(self, pos):
        x = self.pieces[pos[0]][pos[1]].get_possibile_moves(self.pieces, (pos[0],pos[1]))
        result = []
        for e in x:
            check_to_white = self.pieces[pos[0]][pos[1]].is_white
            save_piece = self.pieces[e[0]][e[1]]
            self.move_piece(pos, e)
            if not self.check_for_check(check_to_white):
                result.append(e)
            self.move_piece(e, pos)
            self.pieces[e[0]][e[1]] = save_piece
        return result

    def check_for_promotion(self, player_is_white):
        if player_is_white:
            for i in range(8):
                if self.pieces[i][7] != 0 and self.pieces[i][7].is_promotable:
                    return 7-i
        else:
            for i in range(8):
                if self.pieces[i][0] != 0 and self.pieces[i][0].is_promotable:
                    return i

        return None


    def check_for_check(self, check_to_white):
        if(check_to_white):
            for i in range(8):
                for j in range(8):
                    if self.pieces[i][j] != 0 and not self.pieces[i][j].is_white:
                        x = self.get_piece_possibile_moves_raw((i,j))

                        for e in x:
                            if self.pieces[e[0]][e[1]] != 0 and self.pieces[e[0]][e[1]].is_king and self.pieces[e[0]][e[1]].is_white:
                                return True
        else:
            for i in range(8):
                for j in range(8):
                    if self.pieces[i][j] != 0 and self.pieces[i][j].is_white:
                        x = self.get_piece_possibile_moves_raw((i,j))

                        for e in x:
                            if self.pieces[e[0]][e[1]] != 0 and self.pieces[e[0]][e[1]].is_king and not self.pieces[e[0]][e[1]].is_white:
                                return True
        return False

    def check_for_checkmate(self, checkmate_to_white):
        if not self.check_for_check(checkmate_to_white):
            return False

        if(checkmate_to_white):
            for i in range(8):
                for j in range(8):
                    if self.pieces[i][j] != 0 and self.pieces[i][j].is_white:
                        x = self.get_piece_possibile_moves((i,j))

                        if len(x) > 0:
                            return False
        else:
            for i in range(8):
                for j in range(8):
                    if self.pieces[i][j] != 0 and not self.pieces[i][j].is_white:
                        x = self.get_piece_possibile_moves((i,j))

                        if len(x) > 0:
                            return False
        return True

    def render(self, screen, player_is_white):
        padding = 10
        rect = pygame.Rect((self.pos_x-padding,self.pos_y-padding),(self.cell_width*self.board_width+padding*2,self.cell_height*self.board_height+padding*2))
        pygame.draw.rect(screen,self.color_1 , rect, 0, 0, 10,10,10,10)
        padding = 2
        rect = pygame.Rect((self.pos_x-padding,self.pos_y-padding),(self.cell_width*self.board_width+padding*2,self.cell_height*self.board_height+padding*2))
        pygame.draw.rect(screen, (0,9,0) , rect, 0, 0)

        for i in range(self.board_width):
            for j in range(self.board_height):
                x = self.pos_x + i*self.cell_width
                y = self.pos_y + j*self.cell_height

                rect = pygame.Rect((x,y),(self.cell_width,self.cell_height))

                if (i+j)%2 == 1:
                    color = self.color_1
                else:
                    color = self.color_2

                pygame.draw.rect(screen, color, rect, 0)
        
        font = pygame.font.SysFont('Arial', 16)
        
        padding = 5
        x = self.pos_x + padding
        for i in range(self.board_height):
            y = self.pos_y + i*self.cell_height + padding
            if i%2 == 1:
                color = self.color_2
            else:
                color = self.color_1
                
            if player_is_white:
                txt = font.render(str(self.board_height - i), True, color)
            else:
                txt = font.render(str(i+1), True, color)

            screen.blit(txt, (x,y))

        for i in range(self.board_width):
            if i%2 == 1:
                color = self.color_1
            else:
                color = self.color_2

            if player_is_white:
                txt = font.render(chr(97+i), True, color)
            else:
                txt = font.render(chr(97+self.board_width-i-1), True, color)

            rect = txt.get_rect()

            x = self.pos_x + (i+1)*self.cell_height - padding - rect.width
            y = self.pos_y + self.board_height*self.cell_height - padding -rect.height

            screen.blit(txt, (x,y))
            

    def render_highlighted_cells(self, screen, player_is_white, cells, color):
        for c in cells:
            s = pygame.Surface((self.cell_width, self.cell_height))
            s.set_alpha(180)
            s.fill(color)
            if player_is_white:
                x = self.pos_x + (7-c[0])*self.cell_width
                y = self.pos_y + (7-c[1])*self.cell_height
            else:
                x = self.pos_x + c[0]*self.cell_width
                y = self.pos_y + c[1]*self.cell_height

            screen.blit(s, (x,y))

    def render_possibile_moves_cells(self, screen, player_is_white, cells):
        for c in cells:
            
            s = pygame.Surface((self.cell_width, self.cell_height), pygame.SRCALPHA,32)
            s = s.convert_alpha()
            s.set_alpha(100)
            #s.fill((255,255,255))

            if player_is_white:
                x = self.pos_x + (7-c[0])*self.cell_width 
                y = self.pos_y + (7-c[1])*self.cell_height
            else:
                x = self.pos_x + c[0]*self.cell_width 
                y = self.pos_y + c[1]*self.cell_height
                

            if self.pieces[c[0]][c[1]] == 0:
                pygame.draw.circle(s, (50,50,50), (int(self.cell_width/2), int(self.cell_height/2)), 14)
            else:
                pygame.draw.circle(s, (50,50,50), (int(self.cell_width/2), int(self.cell_height/2)), 34, 5)
            
            screen.blit(s,(x,y))

    def render_dragging_piece(self, screen, cell, pos):
        i = cell[0]
        j = cell[1]
        self.pieces[i][j].render(screen, pos)


    def render_promoting_ui(self, screen, player_is_white, promoting_cell):
        padding = 10
        

        x = self.pos_x + promoting_cell*self.cell_width 
        y = self.pos_y
        rect = pygame.Rect((x-padding,y-padding), (self.cell_width*2+padding*2, self.cell_width*2+padding*2))
        pygame.draw.rect(screen, (0,0,0), rect, 0)
        rect = pygame.Rect((x,y), (self.cell_width*2, self.cell_width*2))
        pygame.draw.rect(screen, (255,255,255), rect, 0)

        if player_is_white:
            queen = pygame.image.load('images/whitequeen.png').convert_alpha()
            rook = pygame.image.load('images/whiterook.png').convert_alpha()
            bishop = pygame.image.load('images/whitebishop.png').convert_alpha()
            knight = pygame.image.load('images/whiteknight.png').convert_alpha()
        else:
            queen = pygame.image.load('images/blackqueen.png').convert_alpha()
            rook = pygame.image.load('images/blackrook.png').convert_alpha()
            bishop = pygame.image.load('images/blackbishop.png').convert_alpha()
            knight = pygame.image.load('images/blackknight.png').convert_alpha()

        sprite_rect = queen.get_rect(center=(x+int(self.cell_width*0.5),y+int(self.cell_height*0.5)))
        screen.blit(queen, sprite_rect)

        sprite_rect = rook.get_rect(center=(x+int(self.cell_width*1.5),y+int(self.cell_height*0.5)))
        screen.blit(rook, sprite_rect)

        sprite_rect = bishop.get_rect(center=(x+int(self.cell_width*0.5),y+int(self.cell_height*1.5)))
        screen.blit(bishop, sprite_rect)

        sprite_rect = knight.get_rect(center=(x+int(self.cell_width*1.5),y+int(self.cell_height*1.5)))
        screen.blit(knight, sprite_rect)


    def render_pieces(self, screen, player_is_white, avoid=[]):
        if player_is_white:
            for i in range(len(self.pieces)):
                for j in range(len(self.pieces[i])):
                    if self.pieces[i][j] != 0 and not (i,j) in avoid:
                        self.pieces[i][j].render(screen, (self.pos_x + (7-i)*self.cell_width + int(self.cell_width/2), self.pos_y + (7-j)*self.cell_height + int(self.cell_height/2)))

        else:
            for i in range(len(self.pieces)):
                for j in range(len(self.pieces[i])):
                    if self.pieces[i][j] != 0 and not (i,j) in avoid:
                        self.pieces[i][j].render(screen, (self.pos_x + i*self.cell_width + int(self.cell_width/2), self.pos_y + j*self.cell_height + int(self.cell_height/2)))