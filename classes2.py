import pygame
import random
from pygame import color
from pygame.font import Font
from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface
from settings import STRUCTURES, Settings

BLOCK_SIZE = Settings.BLOCK_SIZE
V_BOXES = Settings.V_BOXES
H_BOXES = Settings.H_BOXES
BOARD_SIZE = Settings.BOARD_SIZE


class Block():
    """Represents all the boxes in this game"""
    def __init__(self, v_index, h_index, color, screen) -> None:
        self.current_index = v_index, h_index
        self.prev_index = None
        self.screen = screen
        self.topleft_corner = (h_index+1)*BLOCK_SIZE + 10, 709 - (v_index+1)*BLOCK_SIZE
        self.rect = pygame.Rect(self.topleft_corner, (BLOCK_SIZE, BLOCK_SIZE))
        self.color = color
    
    def draw_it(self):
        #print(self.lmt_corner)
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, Settings.WHITE, self.rect, 2)
    
    def update_rect(self, v_index, h_index):
        self.rect.topleft = (h_index+1)*BLOCK_SIZE + 10, 709 - (v_index+1)*BLOCK_SIZE
    
    def move_down(self):
        self.prev_index =  v_index, h_index = self.current_index
        v_index -= 1
        self.current_index = v_index, h_index
        self.update_rect(v_index, h_index)
    
    def move_left(self):
        self.prev_index = v_index, h_index = self.current_index
        h_index -= 1
        self.current_index = v_index, h_index
        self.update_rect(v_index, h_index)
    
    def move_right(self):
        self.prev_index = v_index, h_index = self.current_index
        h_index += 1
        self.current_index = v_index, h_index
        self.update_rect(v_index, h_index)

    def turn_back(self):
        v_index, h_index = self.prev_index
        self.update_rect(v_index, h_index)
        self.current_index = self.prev_index
        self.prev_index = None



class Gboard:
    """The main game board that contains all the standing tetris pieces\n
    shows the pieces to the screen
    """
    def __init__(self, screen, settings: Settings) -> None:
        self.screen = screen
        self.setting = settings
        self.game_board = {}
        for i in range(V_BOXES):     # 32 vertical blocks from down to the top
            self.game_board[i] = set()
    
    
    def add_up(self, blocks: tuple[Block]):
        """Let's a moving piece add itself to the board,\n
        finishes the game if goes over the upper limit(32 block)"""
        for block in blocks:
            v_index = block.current_index[0]
            try:
                self.game_board[v_index].add(block)
            except:
                self.setting.game_over = True
                self.setting.button_active['new game'] = True
    
    def view_board(self):
        """Shows the board to the screen"""
        if self.setting.gameing_mode:
            for key in range(V_BOXES):
                if len(self.game_board[key]) == 0:
                    break
                else:
                    for block in self.game_board[key]:
                        block.draw_it()

    def modify_filled_lines(self):
        """If any line is full then it clears the line\n
        iterates over all the lines above it,takes all the block from the line,\n
        shifts them to one line down and adds to the lower line.\n
        Updates the point.
        Extra Facility: if the line reaches almost last line(V_BOXES),\n
        The game is OVER ! ! !\n
        Before that, it also saves the high score
        """
        for v_index in range(V_BOXES):    # Iterates over all the lines
            if len(self.game_board[v_index]) == 0:
                break
            elif v_index == V_BOXES-1:  # If iteration reaches the last most vertical line
                self.setting.game_over = True
                if self.setting.point > self.setting.high_score:
                    self.setting.high_score = self.setting.point
                # print(self.setting.point, self.setting.high_score)
                break
            elif len(self.game_board[v_index]) == H_BOXES: # if the line is full
                self.game_board[v_index].clear()
                self.setting.update_score()
                next_index = v_index+1   # Line above the current line
                while next_index < V_BOXES:     # Iterates over all the lines above current line
                    if len(self.game_board[next_index]) == 0:
                        break
                    for block in self.game_board[next_index]:
                        block.current_index = block.current_index[0]-1, block.current_index[1]
                        block.update_rect(*block.current_index)
                        self.game_board[next_index-1].add(block)    # Add the block to the lower lone
                    self.game_board[next_index].clear()
                    next_index += 1   # Go to the next line
            



class MovingPiece:
    """This Object contains the piece that is moving"""
    def __init__(self, screen) -> None:
        self.screen = screen
        self.key = random.choice(list(STRUCTURES.keys()))
        self.orient_number = 1
        random_color = random.choice(list(Settings.COLORS.values()))
        self.moving_piece = [Block(v_index, h_index, random_color, screen) for h_index, v_index in STRUCTURES[self.key][1](8, 30)]
        self.left_block, self.right_block, self.down_block = self.moving_piece[0],self.moving_piece[0],self.moving_piece[0]
        self.fix_sideindex()


    def fix_sideindex(self):
        for block in self.moving_piece:
            if block.current_index[0] < self.down_block.current_index[0]:   # current index = vertical index, horizontal index
                self.down_block = block
            if block.current_index[1] < self.left_block.current_index[1]:
                self.left_block = block
            if block.current_index[1] > self.right_block.current_index[1]:
                self.right_block = block

    def show(self):
        for moving_block in self.moving_piece:
            moving_block.draw_it()

    def check_collision(self, gboard: Gboard):
        """Checks if any piece or block touched to a stopped piece og the board\n
        compares all the blocks from moving piece to all the pieces from the gameboard
        returns true if collision occurs
        """
        for moving_block in self.moving_piece:
            for key in range(V_BOXES):
                if len(gboard.game_board[key]) == 0:
                    break
                else:
                    for standing_block in gboard.game_board[key]:
                        if moving_block.rect.colliderect(standing_block.rect):
                            return True
        return False
    
    def move_forward(self, gboard: Gboard):
        """Keeps the main piece moving. Adds up to the game board \n
        if touches any stopped piece. And creates new moving piece
        """
        for moving_block in self.moving_piece:
            moving_block.move_down()
        
        if self.check_collision(gboard) or self.down_block.current_index[0] < 0:
            for moving_block in self.moving_piece:
                moving_block.turn_back()
            gboard.add_up(self.moving_piece)
            self.__init__(self.screen)
    
    def move_sideways(self, gboard: Gboard, direction):
        """to move left or roght"""
        for moving_block in self.moving_piece:
            if direction == "left":
                moving_block.move_left()
            else:
                moving_block.move_right()
        
        if self.check_collision(gboard) or self.left_block.current_index[1] < -1 or self.right_block.current_index[1] > H_BOXES-2:
            # left most index is already 0, and right most index is already H_BOXES
            for moving_block in self.moving_piece:
                moving_block.turn_back()
    

    def jump_down(self, gboard: Gboard):
        while self.down_block.prev_index:
            self.move_forward(gboard)
    

    def change_orientation(self, gboard: Gboard):
        """Creates new orientation from STRUCTURES, based on the moving piece's info and\n
        orient the moving blocks according to it"""
        if self.key == 'o':
            pass
        else:
            self.orient_number += 1
            v_index, h_index =  self.moving_piece[1].current_index
            try:
                orientation = STRUCTURES[self.key][self.orient_number](h_index, v_index)
            except: # If orientation number exceeds total orientations
                self.orient_number = 1
                orientation = STRUCTURES[self.key][self.orient_number](h_index, v_index)
        
            for i in range(4):
                h_index, v_index = orientation[i]
                block = self.moving_piece[i]
                block.prev_index = block.current_index
                block.current_index = v_index, h_index
                block.update_rect(v_index, h_index)
            
            if self.check_collision(gboard):
                for block in self.moving_piece:
                    block.turn_back()
            else:
                self.fix_sideindex()
                # If by chance touches any standing block or touches any side, keep the prev orientation
                if self.down_block.current_index[0] < 0 or self.left_block.current_index[1] < -1 or self.right_block.current_index[1] > H_BOXES-2:
                    for moving_block in self.moving_piece:
                        moving_block.turn_back()



class OptionPallate:
    def __init__(self,screen: pygame.Surface, setting:Settings) -> None:
        self.screen = screen
        self.setting = setting
        self.surface_2 = pygame.Surface(screen.get_rect().size, pygame.SRCALPHA)
        self.surface_2.set_alpha(200)
        #self.start_game_btn = setting.FONT_22.render(
        self.create_pause_button()
        self.create_game_over_button()
        self.create_start_again_win()
        self.create_welcome_text()
        self.create_high_score_text()
        self.create_high_score()
        self.create_your_score_text()
        self.create_yes_no_button()
        self.create_start_button()
        self.create_quit_text()
        self.score_box_rect = self.setting.FONT(64).render(' '*10, True, (1,1,1)).get_rect()
        self.score_box_rect.center = self.score_rect.centerx, self.score_rect.centery + self.score_box_rect.height
    
    def draw_button(self, button, a_rect: Rect, width, curve, button_rect:Rect = None):
        pygame.draw.rect(self.surface_2, (70,70,70), a_rect, 0, curve)
        if button_rect is not None:
            self.surface_2.blit(button, button_rect)
        else:
            self.surface_2.blit(button, a_rect)
        pygame.draw.rect(self.surface_2, Settings.RED, a_rect, width, curve)

    def create_welcome_text(self):
        screen_center = self.screen.get_rect().center
        # The "WELCOME" text, and its rect object
        self.welcome_text = self.setting.FONT(64).render("WELCOME", True, (0,0,255))
        self.welcome_rect = self.welcome_text.get_rect()
        self.welcome_rect.center = screen_center[0], Settings.BOARD_SIZE[1]//3
        # Welcome instruction and its rect
        text2 = "Hit enter to start the game ."
        self.instruction = self.setting.FONT(21).render(text2, True, Settings.BLUE)
        self.inst_rect: Rect = self.instruction.get_rect()
        self.inst_rect.center = self.screen.get_rect().centerx, self.screen.get_rect().width * 4 / 5
    
    def create_high_score_text(self):
        text_hscore = "High Score"
        self.high_score_text = self.setting.FONT(25).render(text_hscore, True, (200, 0, 0))
        self.hscore_rect = self.high_score_text.get_rect()
        x_pos = (690 - Settings.BOARD_SIZE[0])//2 + Settings.BOARD_SIZE[0] + 10
        self.hscore_rect.center = x_pos, Settings.BOARD_SIZE[1]/3.5
    
    def create_high_score(self):
        """Renders the high score to a surface object"""
        high_score_box_rect = self.setting.FONT(25).render(' '*25, True, (50,50,50)).get_rect()
        high_score_box_rect.center = self.hscore_rect.centerx, self.hscore_rect.centery + self.hscore_rect.height + 5
        self.hs_box_rect = high_score_box_rect
        self.high_score = self.setting.FONT(25).render(str(self.setting.high_score), True, (224,0,0))
        self.hs_box_rect2 = self.high_score.get_rect()
        self.hs_box_rect2.center = high_score_box_rect.center

    def create_your_score_text(self):
        self.score_text = self.setting.FONT(28).render("Your Score", True, (200, 0, 0))
        self.score_rect = self.score_text.get_rect()
        self.score_rect.center = self.hscore_rect.center[0], 2*Settings.BOARD_SIZE[1]/3.5
    
    def check_show_score(self):
        score = self.setting.FONT(25).render(str(self.setting.point), True, (224,0,0))
        score_box_rect2 = score.get_rect()
        score_box_rect2.center = self.score_box_rect.center
        pygame.draw.rect(self.screen, (50,50,50), self.score_box_rect, 0, 12)
        self.screen.blit(score, score_box_rect2)
        pygame.draw.rect(self.screen, Settings.RED, self.score_box_rect, 1, 12)

    def create_yes_no_button(self):
        yes_button = self.setting.FONT(18).render('    Yes    ', True, (255,0,0))
        no_button = self.setting.FONT(18).render('    No    ', True, (255,0,0))
        self.yes_rect, self.no_rect = yes_button.get_rect(), no_button.get_rect()
        x_pos, y_pos = self.screen.get_rect().width /3, self.screen.get_rect().height*4 /5
        self.yes_rect.center, self.no_rect.center = (x_pos, y_pos), (x_pos*2, y_pos)
        self.yes_button, self.no_button = yes_button, no_button

    def create_quit_text(self):
        text = "Want to Quit ?"
        self.quit_bg_rect: Rect = self.setting.FONT(35).render(' '*35, True, (0,0,0)).get_rect()
        self.quit_text = self.setting.FONT(25).render(text, True, Settings.RED)
        self.quit_rect: Rect = self.quit_text.get_rect()
        self.quit_rect.center = self.quit_bg_rect.center = self.start_box_rect.center
   
    def create_start_button(self):
        start_box: Rect = self.setting.FONT(35).render(' '*20, True, (0,0,0)).get_rect()
        start_box.center = self.screen.get_rect().centerx ,self.screen.get_rect().height * 2 /3
        self.start_text = self.setting.FONT(25).render("Start Game", True, Settings.RED)
        self.start_rect: Rect = self.start_text.get_rect()
        self.start_rect.center = start_box.center
        self.start_box_rect = start_box
    
    def create_pause_button(self):
        b_pause_color = (200, 0, 0)
        self.bg_pause = (50,50,50)
        self.pause_button = self.setting.FONT(22).render((' '*20+"Paused"+' '*20), True, b_pause_color)
        self.pause_rect: Rect = self.pause_button.get_rect()
        self.pause_rect.center = self.setting.BOARD_SIZE[0]/2 + 10, self.setting.BOARD_SIZE[1]/2

    def create_game_over_button(self):
        button_color = (200, 0, 0)
        self.gov_bg = (50, 50, 50)
        self.gov_button = self.setting.FONT(22).render(' '*11+"Game OVER ! ! !"+' '*9, True, button_color)
        self.gov_rect = self.gov_button.get_rect()
        self.gov_rect.center = self.setting.BOARD_SIZE[0]//2 + 10, self.setting.BOARD_SIZE[1]//3
    
    def create_start_again_win(self):
        # The game over window where "Start Again" & "Quit Game" Buttons are projected
        window_rect: Rect = self.setting.FONT(55).render(' '*25, True, (0,0,0)).get_rect()
        window_rect.center = self.setting.BOARD_SIZE[0]//2 + 10, self.setting.BOARD_SIZE[1] * 2 / 3
        # Buttons
        self.new_game_button: Surface = self.setting.FONT(20).render('   Start New   ', True, (0,0,205))
        self.quite_game_button:Surface = self.setting.FONT(20).render('   Quite Game   ', True, (0,0,205))
        # Rect objects for buttons
        self.new_game_rect = self.new_game_button.get_rect()
        self.quit_game_rect = self.quite_game_button.get_rect()
        self.new_game_rect.centery = self.quit_game_rect.centery = window_rect.centery
        self.new_game_rect.centerx = window_rect.left + window_rect.width * 3 /10
        self.quit_game_rect.centerx = window_rect.left + window_rect.width * 7 /10
        self.gov_window = window_rect

    def show_pallet(self):
        self.screen.blit(self.high_score_text, self.hscore_rect)
        pygame.draw.rect(self.screen, (50,50,50), self.hs_box_rect, 0, 7)
        self.create_high_score()
        self.screen.blit(self.high_score, self.hs_box_rect2)
        pygame.draw.rect(self.screen, Settings.RED, self.hs_box_rect, 1, 7)
        self.screen.blit(self.score_text, self.score_rect)
        self.check_show_score()
        if self.setting.gameing_mode:
            if not self.setting.game_unpaused:
                pygame.draw.rect(self.screen, self.bg_pause, self.pause_rect, 0, 5)
                self.screen.blit(self.pause_button, self.pause_rect)
                pygame.draw.rect(self.screen, Settings.RED, self.pause_rect, 1, 5)
            elif self.setting.game_over:
                # draw the gameover text on screen
                pygame.draw.rect(self.screen, self.gov_bg, self.gov_rect, 0, 5)
                self.screen.blit(self.gov_button, self.gov_rect)
                pygame.draw.rect(self.screen, Settings.RED, self.gov_rect, 1, 5)
                # draw the gameover window
                pygame.draw.rect(self.screen, (40,40,40), self.gov_window, 0, 7)
                pygame.draw.rect(self.screen, self.setting.RED, self.gov_window, 2, 7)
                # draw the "New Game" button on the screen
                self.screen.blit(self.new_game_button, self.new_game_rect)
                pygame.draw.rect(self.screen, self.setting.RED, self.new_game_rect, 1, 4)
                # draw the "Quite Game" button on the screen
                self.screen.blit(self.quite_game_button, self.quit_game_rect)
                pygame.draw.rect(self.screen,self.setting.RED, self.quit_game_rect, 1, 4)
                # Active keys should be marked
                if self.setting.button_active['new game']:
                    pygame.draw.rect(self.screen, self.setting.WHITE, self.new_game_rect, 2, 4)
                else:
                    pygame.draw.rect(self.screen,self.setting.WHITE, self.quit_game_rect, 2, 4)
            

        if self.setting.starting_mode:
            self.surface_2.fill(Settings.BLACK) # 2nd screen coloring
            self.surface_2.blit(self.welcome_text, self.welcome_rect)
            self.surface_2.blit(self.instruction, self.inst_rect)
            self.draw_button(self.start_text, self.start_box_rect, 2, 12, self.start_rect)
            self.screen.blit(self.surface_2, (0,0))

        if self.setting.quiting_mode:
            self.surface_2.fill(Settings.BLACK) # 2nd screen coloring
            # active buttons should be highlighted
            if self.setting.button_active['yes']:
                pygame.draw.rect(self.screen, self.setting.WHITE, self.yes_rect, 0, 7)
            else:
                pygame.draw.rect(self.screen,self.setting.WHITE, self.no_rect, 0, 7)
            self.draw_button(self.yes_button, self.yes_rect, 1, 7)  # "Yes" Button
            self.draw_button(self.no_button, self.no_rect, 1, 7,) # "No" button
            # Wanna Quit ? - text
            self.draw_button(self.quit_text, self.quit_bg_rect, 3, 15, self.quit_rect)
            self.screen.blit(self.surface_2, (0,0))
