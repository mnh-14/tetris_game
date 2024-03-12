import sys
import pygame
from classes2 import MovingPiece, Gboard
from settings import Settings

def check_events(gboard: Gboard, moving_piece:MovingPiece, setting: Settings):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                setting.quiting_mode = True
                setting.game_unpaused = False
                setting.reset_buttons()
                setting.button_active['new game'] = True
                check_quite_prev_mode(setting)
            if event.key == pygame.K_LEFT:
                if setting.quiting_mode:
                    button_active_swap(setting, 'yes', 'no')
                elif setting.game_over:
                    button_active_swap(setting, 'new game', 'quit game')
                elif setting.game_unpaused: moving_piece.move_sideways(gboard, "left")
            if event.key == pygame.K_RIGHT:
                if setting.quiting_mode:
                    button_active_swap(setting, 'yes', 'no')
                elif setting.game_over:
                    button_active_swap(setting, 'new game', 'quit game')
                elif setting.game_unpaused: moving_piece.move_sideways(gboard, "right")
            if event.key == pygame.K_DOWN:
                if setting.game_unpaused: moving_piece.jump_down(gboard)
            if event.key == pygame.K_UP:
                if setting.gameing_mode and not setting.game_over:
                    if setting.game_unpaused: moving_piece.change_orientation(gboard)
            if event.key == pygame.K_SPACE:
                if setting.gameing_mode and not setting.game_over:
                    if not setting.game_unpaused: setting.game_unpaused = True
                    else: setting.game_unpaused = False
            if event.key == pygame.K_RETURN:
                swap_modes(gboard, moving_piece, setting)


def button_active_swap(setting: Settings, b1, b2):
    if setting.button_active[b1]:
        setting.button_active[b1] = False
        setting.button_active[b2] = True
    else:
        setting.button_active[b2] = False
        setting.button_active[b1] = True

def swap_modes(gboard: Gboard, moving_piece: MovingPiece , setting: Settings):
    if setting.quiting_mode:
        if setting.button_active['yes']:
            setting.save_high_score()
            sys.exit()
        else:
            setting.quiting_mode = False
            setting.reset_buttons()
            check_quite_prev_mode(setting)
    elif setting.starting_mode:
        setting.gameing_mode = True
        setting.starting_mode = False
        setting.reset_buttons()
    elif setting.game_over:
        if setting.button_active['new game']:
            setting.reset_buttons()
            for v_index, h_lines in gboard.game_board.items():
                if len(h_lines) == 0: break
                h_lines.clear()
            moving_piece.__init__(gboard.screen)
            setting.game_over = False
            setting.reset_buttons()
            setting.set_defaults()
        else:
            setting.save_high_score()
            sys.exit()


def check_quite_prev_mode(setting: Settings):
    if setting.quiting_mode:
        if setting.starting_mode:
            setting.prev_mode = 'starting mode'
            setting.starting_mode = False
        elif setting.game_over:
            setting.prev_mode = 'game over mode'
    else:
        if setting.prev_mode == 'starting mode':
            setting.starting_mode = True
            setting.button_active['start game'] = True
        elif setting.prev_mode == 'game over mode':
            setting.game_unpaused = True
            setting.button_active['new game'] = True
