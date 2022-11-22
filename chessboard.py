import pygame
import math
from pieces.piece import Piece
from pieces.king import King


class Chessboard():
    def __init__(self, pos, board_size , cell_size, board_padding=10):
        self.board_padding = board_padding
        self.board_width, self.board_height = board_size

        self.__capture = None
        
        self.set_cell_size(cell_size)
        self.set_pos(pos)

        # create the actual matrix:
        self.pieces = []
        for _ in range(self.board_width):
            temp = []
            for _ in range(self.board_height):
                temp.append(0)
            self.pieces.append(temp)

    def get_capture(self):
        capture = self.__capture
        self.__capture = None
        return capture

    def get_rect(self):
        return pygame.Rect(self.pos_x-self.board_padding, self.pos_y-self.board_padding, self.board_width*self.cell_width+2*self.board_padding, self.board_height*self.cell_height+2*self.board_padding)

    def set_pos(self, pos):
        self.pos_x, self.pos_y = pos
        self.pos_x -= int((self.board_width/2) * self.cell_width)
        self.pos_y -= int((self.board_height/2) * self.cell_height)

    def set_cell_size(self, cell_size):
        self.cell_width = self.cell_height = cell_size
    
    def set_colors(self, color_1, color_2):
        self.color_1 = color_1
        self.color_2 = color_2

    def get_piece(self, cell):
        x,y = cell
        if self.pieces[x][y] == 0:
            return None
        return self.pieces[x][y]

    # returns a tuple which represents the coordinates of the cell the position falls
    def get_cell_by_position(self, pos, player_is_white, limit=True):
        tx = pos[0] - self.pos_x
        ty  = pos[1] - self.pos_y
        
        x = math.floor(tx/self.cell_width)
        y = math.floor(ty/self.cell_height)

        if (x < 0 or y < 0 or x >= self.board_width or y >= self.board_height) and limit:
            return None

        if player_is_white:
            return (x,self.board_height-y-1)
        else:
            return (self.board_width-x-1, y)

    def remove_piece(self, pos, record_capture=False):
        if record_capture:
            p = self.get_piece(pos)
            if p != None:
                self.__capture = p.get_code()
        self.add_piece(pos, 0)

    def add_piece(self, pos, piece, record_capture=False):
        if record_capture:
            p = self.get_piece(pos)
            if p != None:
                self.__capture = p.get_code()
        self.pieces[pos[0]][pos[1]] = piece

    def get_cell_name(self, cell):
        x,y = cell
        return chr(x+97) + str(y+1)

    def get_move_code(self,starting_cell, destination_cell):
        if self.get_piece(starting_cell) == 0:
            return None
        code = self.get_piece(starting_cell).get_code().upper()
        
        if code == 'K' and abs(starting_cell[0]-destination_cell[0]) == 2:
            if destination_cell[0] == 2:
                code = 'O-O-O'
            else:
                code = 'O-O'

        else:
            disambiguating = ''

            same_pieces = self.get_pieces_by_piece_code(code[0],self.get_piece(starting_cell).is_white)
            same_pieces.remove(starting_cell)
            for p in same_pieces:
                pm = self.get_piece_possible_moves(p)
                if destination_cell in pm:
                    if p[0] == starting_cell[0]:
                        disambiguating = self.get_cell_name(starting_cell)
                        break
                    else:
                        disambiguating = self.get_cell_name(starting_cell)[0]

            code += disambiguating

            if self.get_piece(destination_cell) != None:
                code += 'x'
            else:
                if code[0] == 'P' and starting_cell[0] != destination_cell[0]:
                    code += 'x'

            code += self.get_cell_name(destination_cell)

            if code[0] == 'P':
                code = code[1:]
        
        return code


    def move_piece(self, starting_pos, destination_pos, definitive=False, castling_check=False, en_passant=False):
        if castling_check:
            if self.pieces[starting_pos[0]][starting_pos[1]].is_king and abs(starting_pos[0]-destination_pos[0]) == 2:
                if starting_pos[0] < destination_pos[0]:
                    self.add_piece((destination_pos[0]-1, destination_pos[1]), self.pieces[self.board_height-1][destination_pos[1]])
                    self.remove_piece((self.board_width-1, destination_pos[1]))                    
                else:
                    self.add_piece((destination_pos[0]+1, destination_pos[1]), self.pieces[0][destination_pos[1]])
                    self.remove_piece((0, destination_pos[1]))

        if en_passant:
            if self.pieces[starting_pos[0]][starting_pos[1]].is_promotable and starting_pos[0] != destination_pos[0] and self.pieces[destination_pos[0]][destination_pos[1]] == 0:
                self.remove_piece((destination_pos[0], starting_pos[1]), definitive)


        self.add_piece(destination_pos, self.pieces[starting_pos[0]][starting_pos[1]], definitive)
        self.remove_piece(starting_pos)
        if definitive:
            self.get_piece(destination_pos).move()
            for i in range(self.board_width):
                for j in range(self.board_height):
                    if self.pieces[i][j] != 0:
                        self.pieces[i][j].can_be_captured_en_passant = False
            if self.pieces[destination_pos[0]][destination_pos[1]].is_promotable and abs(starting_pos[1]-destination_pos[1]) == 2:
                self.pieces[destination_pos[0]][destination_pos[1]].can_be_captured_en_passant = True
        
    def get_player_possible_moves(self, white):
        moves = []
        
        for i in range(self.board_width):
            for j in range(self.board_height):
                if self.pieces[i][j] != 0 and not (self.pieces[i][j].is_white ^ white):
                    pm = self.get_piece_possible_moves((i,j))
                    for m in pm:
                        moves.append(((i,j),m))
        return moves

    def get_piece_possible_moves_raw(self, pos):
        x = self.pieces[pos[0]][pos[1]].get_possible_moves(self.pieces, (pos[0],pos[1]))
        
        return x

    def get_pieces_by_piece_code(self, piece_code, white):
        ret = []
        for i in range(self.board_width):
            for j in range(self.board_height):
                if self.pieces[i][j] != 0:
                    if (not (self.pieces[i][j].is_white ^ white)) and self.pieces[i][j].get_code().lower() == piece_code.lower():
                        ret.append((i,j))
        return ret

    def get_piece_possible_moves(self, pos):
        
        check_to_white = self.pieces[pos[0]][pos[1]].is_white
        

        if self.pieces[pos[0]][pos[1]].is_king:
            self.pieces[pos[0]][pos[1]].check = False
            if self.check_for_check(check_to_white):
                self.pieces[pos[0]][pos[1]].check = True
        x = self.pieces[pos[0]][pos[1]].get_possible_moves(self.pieces, (pos[0],pos[1]))
        result = []

        for e in x:
            # check if the current move is castling
            if self.pieces[pos[0]][pos[1]].is_king and abs(e[0]-pos[0]) == 2:
                self.move_piece(pos, (e[0]+(pos[0]-e[0])//2,e[1]), False)
                if not self.check_for_check(check_to_white):
                    self.move_piece((e[0]+(pos[0]-e[0])//2,e[1]), pos, False)
                    self.move_piece(pos, e, False)
                    if not self.check_for_check(check_to_white):
                        result.append(e)
                    self.move_piece(e,pos, False)
                else:
                    self.move_piece((e[0]+(pos[0]-e[0])//2,e[1]), pos, False)

            elif self.pieces[pos[0]][pos[1]].is_promotable and e[0] != pos[0] and self.pieces[e[0]][e[1]] == 0:
                save_piece = self.pieces[e[0]][pos[1]]
                self.remove_piece((e[0],pos[1]))

                self.move_piece(pos, e, False)
                if not self.check_for_check(check_to_white):
                    result.append(e)
                
                self.move_piece(e, pos, False)
                self.pieces[e[0]][pos[1]] = save_piece
            else:
                save_piece = self.pieces[e[0]][e[1]]
                
                self.move_piece(pos, e, False)
                if not self.check_for_check(check_to_white):
                    result.append(e)
                
                self.move_piece(e, pos, False)
                self.pieces[e[0]][e[1]] = save_piece
        
        return result

    def check_for_promotion(self):
        for i in range(self.board_width):
            if self.pieces[i][0] != 0 and self.pieces[i][0].is_promotable:
                return i
            if self.pieces[i][7] != 0 and self.pieces[i][7].is_promotable:
                return i

        return None


    def check_for_check(self, check_to_white):
        if(check_to_white):
            for i in range(self.board_width):
                for j in range(self.board_height):
                    if self.pieces[i][j] != 0 and not self.pieces[i][j].is_white:
                        x = self.get_piece_possible_moves_raw((i,j))
                        for e in x:
                            if self.pieces[e[0]][e[1]] != 0 and self.pieces[e[0]][e[1]].is_king and self.pieces[e[0]][e[1]].is_white:
                                return True
            
        else:
            for i in range(self.board_width):
                for j in range(self.board_height):
                    if self.pieces[i][j] != 0 and self.pieces[i][j].is_white:
                        x = self.get_piece_possible_moves_raw((i,j))
                        for e in x:
                            if self.pieces[e[0]][e[1]] != 0 and self.pieces[e[0]][e[1]].is_king and not self.pieces[e[0]][e[1]].is_white:
                                return True

        
        return False

    def has_legal_moves(self, white):
        for i in range(self.board_width):
            for j in range(self.board_height):
                if (self.pieces[i][j] != 0 and self.pieces[i][j].is_white and white) or (self.pieces[i][j] != 0 and not self.pieces[i][j].is_white and not white):
                    x = self.get_piece_possible_moves((i,j))

                    if len(x) > 0:
                        return True


    def check_for_checkmate(self, checkmate_to_white):
        if not self.check_for_check(checkmate_to_white):
            return False

        return not self.has_legal_moves(checkmate_to_white)

    def check_for_stalemate(self, stalemate_to_white):
        if self.check_for_check(stalemate_to_white):
            return False
        
        return not self.has_legal_moves(stalemate_to_white)

    def render(self, screen, player_is_white):
        padding = self.board_padding
        rect = pygame.Rect((self.pos_x-padding,self.pos_y-padding),(self.cell_width*self.board_width+padding*2,self.cell_height*self.board_height+padding*2))
        pygame.draw.rect(screen,self.color_1 , rect, 0, 0, 10,10,10,10)
        padding = 2
        rect = pygame.Rect((self.pos_x-padding,self.pos_y-padding),(self.cell_width*self.board_width+padding*2,self.cell_height*self.board_height+padding*2))
        pygame.draw.rect(screen, (0,0,0) , rect, 0, 0)

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
            

    def render_highlighted_cells(self, screen, player_is_white, cells, color, highlighting_alpha=130):
        for c in cells:
            s = pygame.Surface((self.cell_width, self.cell_height))
            s.set_alpha(highlighting_alpha)
            s.fill(color)
            if player_is_white:
                x = self.pos_x + c[0]*self.cell_width
                y = self.pos_y + (self.board_height-c[1]-1)*self.cell_height
            else:
                x = self.pos_x + (self.board_width-c[0]-1)*self.cell_width
                y = self.pos_y + c[1]*self.cell_height

            screen.blit(s, (x,y))

    def render_possible_moves_cells(self, screen, player_is_white, cells):
        for c in cells:
            s = pygame.Surface((self.cell_width, self.cell_height), pygame.SRCALPHA,32)
            s = s.convert_alpha()
            s.set_alpha(100)

            if player_is_white:
                x = self.pos_x + c[0]*self.cell_width                 
                y = self.pos_y + (self.board_height-c[1]-1)*self.cell_height
            else:
                x = self.pos_x + (self.board_width-c[0]-1)*self.cell_width

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


    def render_promoting_ui(self, screen, player_is_white, view_as_white, promoting_cell):
        padding = self.board_padding

        if not view_as_white:
                promoting_cell = 7-promoting_cell

        if player_is_white ^ view_as_white:
            
            y = self.pos_y + (self.cell_height* (self.board_height-2))
            x = self.pos_x + (promoting_cell)*self.cell_width 
        else:
            #promoting_cell = self.board_width-promoting_cell-1
            y = self.pos_y
            x = self.pos_x + promoting_cell*self.cell_width 
        
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
                        self.pieces[i][j].render(screen, (self.pos_x + i*self.cell_width + int(self.cell_width/2), self.pos_y + (self.board_height-j-1)*self.cell_height + int(self.cell_height/2)))

        else:
            for i in range(len(self.pieces)):
                for j in range(len(self.pieces[i])):
                    if self.pieces[i][j] != 0 and not (i,j) in avoid:
                        self.pieces[i][j].render(screen, (self.pos_x + (self.board_width-i-1)*self.cell_width + int(self.cell_width/2), self.pos_y + j*self.cell_height + int(self.cell_height/2)))


    def render_arrows(self, screen, player_is_white, arrows, color, arrows_alpha=140):
        s = pygame.Surface((self.cell_width*self.board_width, self.cell_width*self.board_height), pygame.SRCALPHA)
        s.fill((255,255,255,0))

        for a in arrows:
            ax,ay,bx,by = a

            base_length = self.cell_width/5
            arrow_base_2_length = self.cell_width/2
            starting_cell_center = (self.cell_width*(ax+0.5), (self.cell_height*self.board_height)-(self.cell_height*(ay+0.5)))
            destination_cell_center = (self.cell_width*(bx+0.5), (self.cell_height*self.board_height)-(self.cell_height*(by+0.5)))
            base_center_distance_from_cell_center = self.cell_width/3
            
            if (abs(ax - bx) == 2 and abs(ay - by) == 1):
                # horse jump arrow (horizontal)
                base_center = (starting_cell_center[0] - base_center_distance_from_cell_center*((ax-bx)/abs(ax-bx)), starting_cell_center[1] )
                base_point_1 = (base_center[0], base_center[1] - base_length/2)
                base_point_2 = (base_center[0], base_center[1] + base_length/2)

                arrow_bases_center = (destination_cell_center[0], destination_cell_center[1] - base_center_distance_from_cell_center*((ay-by)/abs(ay-by)))
                arrow_base_1_point_1 = (arrow_bases_center[0] - base_length/2*((ax-bx)/abs(ax-bx))*((ay-by)/abs(ay-by)), arrow_bases_center[1])
                arrow_base_1_point_2 = (arrow_bases_center[0] + base_length/2*((ax-bx)/abs(ax-bx))*((ay-by)/abs(ay-by)), arrow_bases_center[1])
                arrow_base_2_point_1 = (arrow_bases_center[0] - arrow_base_2_length/2*((ax-bx)/abs(ax-bx))*((ay-by)/abs(ay-by)), arrow_bases_center[1])
                arrow_base_2_point_2 = (arrow_bases_center[0] + arrow_base_2_length/2*((ax-bx)/abs(ax-bx))*((ay-by)/abs(ay-by)), arrow_bases_center[1])

                turn_cell_center = (destination_cell_center[0], starting_cell_center[1])
                
                turn_point_1 = (turn_cell_center[0] - (base_length/2)*((bx-ax)/abs(bx-ax))*((by-ay)/abs(by-ay)) , turn_cell_center[1] - (base_length/2))
                turn_point_2 = (turn_cell_center[0] + (base_length/2)*((bx-ax)/abs(bx-ax))*((by-ay)/abs(by-ay)) , turn_cell_center[1] + (base_length/2))

                pygame.draw.polygon(s, (*color, arrows_alpha), [turn_point_2, base_point_2, base_point_1, turn_point_1, arrow_base_1_point_1, arrow_base_2_point_1, destination_cell_center, arrow_base_2_point_2, arrow_base_1_point_2])
            elif (abs(ax - bx) == 1 and abs(ay - by) == 2):
                # horse jump arrow (vertical)
                base_center = (starting_cell_center[0], starting_cell_center[1] + base_center_distance_from_cell_center*((ay-by)/abs(ay-by)))
                base_point_1 = (base_center[0] + base_length/2, base_center[1])
                base_point_2 = (base_center[0] - base_length/2, base_center[1])

                arrow_bases_center = (destination_cell_center[0] + base_center_distance_from_cell_center*((ax-bx)/abs(ax-bx)), destination_cell_center[1])
                arrow_base_1_point_1 = (arrow_bases_center[0], arrow_bases_center[1]+base_length/2*((ax-bx)/abs(ax-bx))*((ay-by)/abs(ay-by)))
                arrow_base_1_point_2 = (arrow_bases_center[0], arrow_bases_center[1]-base_length/2*((ax-bx)/abs(ax-bx))*((ay-by)/abs(ay-by)))
                arrow_base_2_point_1 = (arrow_bases_center[0], arrow_bases_center[1]+arrow_base_2_length/2*((ax-bx)/abs(ax-bx))*((ay-by)/abs(ay-by)))
                arrow_base_2_point_2 = (arrow_bases_center[0], arrow_bases_center[1]-arrow_base_2_length/2*((ax-bx)/abs(ax-bx))*((ay-by)/abs(ay-by)))

                turn_cell_center = (starting_cell_center[0], destination_cell_center[1])
                
                turn_point_1 = (turn_cell_center[0] + (base_length/2), turn_cell_center[1] + (base_length/2)*((bx-ax)/abs(bx-ax))*((by-ay)/abs(by-ay)))
                turn_point_2 = (turn_cell_center[0] - (base_length/2), turn_cell_center[1] - (base_length/2)*((bx-ax)/abs(bx-ax))*((by-ay)/abs(by-ay)))

                pygame.draw.polygon(s, (*color, arrows_alpha), [turn_point_2, base_point_2, base_point_1, turn_point_1, arrow_base_1_point_1, arrow_base_2_point_1, destination_cell_center, arrow_base_2_point_2, arrow_base_1_point_2])
            else:
                # straight arrow
                arrow_length = math.sqrt((ax-bx)**2 + (ay-by)**2)
                sin = (by-ay)/arrow_length
                cos = (bx-ax)/arrow_length
                
                if sin != 0:
                    angle = (sin/abs(sin))*math.acos(cos)
                else:
                    angle = math.acos(cos)
                base_slope_angle = angle - (math.pi/2)
                                
                base_center = (starting_cell_center[0] + math.cos(angle)*base_center_distance_from_cell_center, starting_cell_center[1] - math.sin(angle)*base_center_distance_from_cell_center)

                base_point_1 = (base_center[0] + math.cos(base_slope_angle)*(base_length/2), base_center[1] - math.sin(base_slope_angle)*(base_length/2))
                base_point_2 = (base_center[0] + math.cos(base_slope_angle + math.pi)*(base_length/2), base_center[1] - math.sin(base_slope_angle + math.pi)*(base_length/2))

                arrow_bases_center = (destination_cell_center[0] + math.cos(angle+math.pi)*base_center_distance_from_cell_center, destination_cell_center[1] - math.sin(angle+math.pi)*base_center_distance_from_cell_center)

                arrow_base_1_point_1 = (arrow_bases_center[0] + math.cos(base_slope_angle)*(base_length/2), arrow_bases_center[1] - math.sin(base_slope_angle)*(base_length/2))
                arrow_base_1_point_2 = (arrow_bases_center[0] + math.cos(base_slope_angle + math.pi)*(base_length/2), arrow_bases_center[1] - math.sin(base_slope_angle + math.pi)*(base_length/2))
                arrow_base_2_point_1 = (arrow_bases_center[0] + math.cos(base_slope_angle)*(arrow_base_2_length/2), arrow_bases_center[1] - math.sin(base_slope_angle)*(arrow_base_2_length/2))
                arrow_base_2_point_2 = (arrow_bases_center[0] + math.cos(base_slope_angle + math.pi)*(arrow_base_2_length/2), arrow_bases_center[1] - math.sin(base_slope_angle + math.pi)*(arrow_base_2_length/2))

                pygame.draw.polygon(s, (*color, arrows_alpha), [base_point_2, base_point_1, arrow_base_1_point_1, arrow_base_2_point_1, destination_cell_center, arrow_base_2_point_2, arrow_base_1_point_2])

        if not player_is_white:
            s = pygame.transform.rotate(s, 180)
        screen.blit(s, (self.pos_x, self.pos_y))