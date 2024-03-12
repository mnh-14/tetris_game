import pygame
import sys

from pygame import display
from classes2 import Gboard, MovingPiece, OptionPallate
import events
from settings import Settings

pygame.init()
screen = display.set_mode((700, 720))
display.set_caption("Tetris", "icon.ico")
black = 0,0,0

FPS = 60
game_setting = Settings()
fps_clock = pygame.time.Clock()
gboard = Gboard(screen, game_setting)
moving_piece = MovingPiece(screen)
pallate = OptionPallate(screen, game_setting)
game_setting.frames_counter = 0

while True:
    screen.fill(black)
    events.check_events(gboard, moving_piece, game_setting)
    
    if game_setting.gameing_mode:
        gboard.view_board()
        if game_setting.game_unpaused and not game_setting.game_over:
            gboard.modify_filled_lines()
            moving_piece.show()
            game_setting.frames_counter += 1
            if game_setting.frames_counter == game_setting.frames_per_action:
                moving_piece.move_forward(gboard)
                game_setting.frames_counter = 0
    
    pygame.draw.rect(screen, Settings.RED, pygame.Rect((10,5), Settings.BOARD_SIZE), 2)
    pallate.show_pallet()

    display.flip()
    fps_clock.tick(FPS)